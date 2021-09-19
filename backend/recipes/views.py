from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (exceptions, filters, mixins, permissions, serializers, viewsets, status)
from rest_framework.response import Response
from rest_framework.views import APIView
from .filters import IngredientsFilter, RecipeFilter
from .models import Ingredient, RecipeIngredients, Tag, Recipe, Favorite, ShoppingList
from .serializers import IngredientsSerializer, TagsSerializer, ShowRecipeSerializer, AddRecipeSerializer, FavouriteSerializer, ShoppingListSerializer
from .permissions import IsAuthorOrAdmin
from foodgram.pagination import CustomPageNumberPaginator


class RetriveAndListViewSet(
        mixins.ListModelMixin,
        mixins.RetrieveModelMixin,
        viewsets.GenericViewSet):
    pass


class IngredientsViewSet(RetriveAndListViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientsSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_class = IngredientsFilter


class TagsViewSet(RetriveAndListViewSet):
    queryset = Tag.objects.all()
    serializer_class =TagsSerializer
    permission_classes = [permissions.AllowAny]


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all().order_by('id')
    serializer_class = ShowRecipeSerializer
    permission_classes = [IsAuthorOrAdmin]
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter
    pagination_class = CustomPageNumberPaginator

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ShowRecipeSerializer
        else:
            return AddRecipeSerializer


class FavoriteViewSet(APIView):

    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request, recipe_id):
        data = {'user': request.user.id, 'recipe': recipe_id}
        serializer = FavouriteSerializer(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, recipe_id):
        data = {'user': request.user.id, 'recipe': recipe_id}
        user = request.user
        recipe = get_object_or_404(Recipe, id=recipe_id)
        serializer = FavouriteSerializer(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        Favorite.objects.get(user=user, recipe=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ShoppingListViewSet(APIView):

    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request, recipe_id):
        data = {'user': request.user.id, 'recipe': recipe_id}
        serializer = ShoppingListSerializer(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, recipe_id):
        data = {'user': request.user.id, 'recipe': recipe_id}
        user = request.user
        recipe = get_object_or_404(Recipe, id=recipe_id)
        serializer = ShoppingListSerializer(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        ShoppingList.objects.get(user=user, recipe=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class DownloadShoppingCart(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        shopping_cart = request.user.shopping_list.all()
        buying_list = {}

        for item in shopping_cart:
            ingredients = RecipeIngredients.objects.filter(recipe=item.recipe)
            for ingredient in ingredients:
                amount = ingredient.amount
                name = ingredient.ingredient.name
                measurement_unit = ingredient.ingredient.measurement_unit

                if name not in buying_list:
                    buying_list[name] = {
                        'measurement_unit': measurement_unit,
                        'amount': amount
                    }
                else:
                    buying_list[name]['amount'] = (buying_list[name]['amount']
                                                   + amount)

        wishlist = []
        for item in buying_list:
            wishlist.append(f'{item} - {buying_list[item]["amount"]} '
                            f'{buying_list[item]["measurement_unit"]} \n')

        response = HttpResponse(wishlist, 'Content-Type: text/plain')
        response['Content-Disposition'] = 'attachment; filename="wishlist.txt"'
        return response
