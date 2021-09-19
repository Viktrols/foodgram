from django.contrib import admin
from .models import (Ingredient, Tag, Recipe, RecipeTags,
                     RecipeIngredients, Favorite, ShoppingList)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'measurement_unit')


class RecipeIngredientsInline(admin.TabularInline):
    model = RecipeIngredients
    min_num = 1
    extra = 1


class RecipeTagsInline(admin.TabularInline):
    model = RecipeTags
    min_num = 1
    extra = 0


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'author')
    inlines = (RecipeIngredientsInline, RecipeTagsInline)


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'recipe')


@admin.register(ShoppingList)
class ShoppingListAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'recipe')
