from django.contrib.auth import get_user_model
from django.db.models import F
from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField

from django.shortcuts import get_object_or_404
from users.serializers import UserSerializer
from .models import Ingredient, Tag, Recipe, RecipeIngredients, Favorite, ShoppingList

User = get_user_model()

class IngredientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class ShowRecipeIngredientsSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(source='ingredient.measurement_unit')
    
    class Meta:
        model = RecipeIngredients
        fields = ('id', 'name', 'measurement_unit', 'amount')


class ShowRecipeSerializer(serializers.ModelSerializer):
    tags = TagsSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)
    ingredients = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()


    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'name',
                  'image', 'text', 'cooking_time', 'is_favorited', 'is_in_shopping_cart')

    def get_ingredients(self, obj):
        ingredients = RecipeIngredients.objects.filter(recipe=obj)
        return ShowRecipeIngredientsSerializer(ingredients, many=True).data

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return Favorite.objects.filter(recipe=obj, user=request.user).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return ShoppingList.objects.filter(recipe=obj, user=request.user).exists()


class AddRecipeIngredientsSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    amount = serializers.IntegerField()

    class Meta:
        model = RecipeIngredients
        fields = ('id', 'amount')


class AddRecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    author = UserSerializer(read_only=True)
    ingredients = AddRecipeIngredientsSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True)
    cooking_time = serializers.IntegerField()


    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'name',
                 'image', 'text', 'cooking_time'
                )

    def validate(self, data):
        ingredients = self.initial_data.get('ingredients')
        if ingredients == []:
            raise serializers.ValidationError(
                {'ingredients': ('Нужно выбрать минимум 1 ингридиент!')}
                )
        for ingredient in ingredients:
            if int(ingredient['amount']) <= 0:
                raise serializers.ValidationError(
                    {'ingredients': ('Количество не может быть отрицательным числом или нулем')}
                    )
        return data


    def validate_cooking_time(self, data):
        if data <= 0:
            raise serializers.ValidationError(
                'Время готовки не может быть отрицательным числом или нулем'
            )
        return data
    

    def add_recipe_ingredients(self, ingredients, recipe):
        for ingredient in ingredients:
            ingredient_id = ingredient['id']
            amount = ingredient['amount']
            if RecipeIngredients.objects.filter(recipe=recipe, ingredient=ingredient_id).exists():
                amount += F('amount')
            RecipeIngredients.objects.update_or_create(recipe=recipe, ingredient=ingredient_id, defaults={'amount': amount})


    def create(self, validated_data):
        author = self.context.get('request').user
        tags_data = validated_data.pop('tags')
        ingredients_data = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(author=author, **validated_data)      
        self.add_recipe_ingredients(ingredients_data, recipe)
        recipe.tags.set(tags_data)
        return recipe


    def update(self, recipe, validated_data):
        recipe.name = validated_data.get('name', recipe.name)
        recipe.text = validated_data.get('text', recipe.text)
        recipe.cooking_time = validated_data.get('cooking_time',recipe.cooking_time)
        recipe.image = validated_data.get('image', recipe.image)
        if 'ingredients' in self.initial_data:
            ingredients = validated_data.pop('ingredients')
            recipe.ingredients.clear()
            self.add_recipe_ingredients(ingredients, recipe)           
        if 'tags' in self.initial_data:
            tags_data = validated_data.pop('tags')
            recipe.tags.set(tags_data)       
        recipe.save()
        return recipe


    def to_representation(self, recipe):
        data = ShowRecipeSerializer( recipe, context={'request': self.context.get('request')}).data
        return data


class ShowRecipeLightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class FavouriteSerializer(serializers.ModelSerializer):
    recipe = serializers.PrimaryKeyRelatedField(queryset=Recipe.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    class Meta:
        model = Favorite
        fields = ('user', 'recipe')
    def validate(self, data):
        user = self.context.get('request').user
        recipe_id = data['recipe'].id
        if (self.context.get('request').method == 'GET'
                and ShoppingList.objects.filter(user=user, recipe__id=recipe_id).exists()):
            raise serializers.ValidationError('Рецепт уже добавлен в список покупок')
        recipe = get_object_or_404(Recipe, id=recipe_id)

        if (self.context.get('request').method == 'DELETE'
                and not Favorite.objects.filter( user=user, recipe=recipe).exists()):
            raise serializers.ValidationError('Этот рецепт не был добавлен в избранное')
        return data

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return ShowRecipeLightSerializer( instance.recipe, context=context).data


class ShoppingListSerializer(serializers.ModelSerializer):
    recipe = serializers.PrimaryKeyRelatedField(queryset=Recipe.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = ShoppingList
        fields = ('user', 'recipe')

    def validate(self, data):
        user = self.context.get('request').user
        recipe_id = data['recipe'].id
        if (self.context.get('request').method == 'GET'
                and ShoppingList.objects.filter(user=user,
                                            recipe__id=recipe_id).exists()):
            raise serializers.ValidationError('Рецепт уже добавлен в список покупок')

        if (self.context.get('request').method == 'DELETE'
                and not ShoppingList.objects.filter(user=user, recipe_id=recipe_id).exists()):
            raise serializers.ValidationError('Этот рецепт не был добавлен в ваш список покупок')

        return data

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return ShowRecipeLightSerializer(instance.recipe, context=context).data
