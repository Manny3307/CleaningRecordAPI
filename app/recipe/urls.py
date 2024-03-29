from django.urls import path, include
from rest_framework import routers, urlpatterns
from rest_framework.routers import DefaultRouter
from recipe import views

router = routers.DefaultRouter()
router.register('tags', views.TagViewSets)
router.register('ingredients', views.IngredientViewSets)
router.register('recipes', views.RecipeViewSet)

app_name = 'recipe'

urlpatterns = [
    path('', include(router.urls)),
]