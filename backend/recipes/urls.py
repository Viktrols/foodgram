from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register('ingredients', views.IngredientsViewSet,
                basename='ingredients')
router.register('tags', views.TagsViewSet, basename='tags')
router.register('recipes', views.RecipeViewSet, basename='recipes')


urlpatterns = [
     path('recipes/<int:recipe_id>/favorite/', views.FavoriteViewSet.as_view(),
         name='favorite'),
     path('recipes/download_shopping_cart/',
         views.DownloadShoppingCart.as_view(), name='dowload_shopping_cart'),
     path('recipes/<int:recipe_id>/shopping_cart/',
         views.ShoppingListViewSet.as_view(), name='shopping_cart'),
     path('', include(router.urls)),
]
