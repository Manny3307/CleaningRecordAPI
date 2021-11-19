from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from core.models import Recipe, Tag, Ingredient
from recipe import serializers

class BaseRecipeAttrViewsets(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    #Base viewset for user owned recipe attributes
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        #Return Objects for the current authenticated user only
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        #Create a new tag
        serializer.save(user=self.request.user)

class TagViewSets(BaseRecipeAttrViewsets):
    #Manage Tags in the Database
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer


class IngredientViewSets(BaseRecipeAttrViewsets):
    #Manage Ingredient in the Database
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer


class RecipeViewSets(BaseRecipeAttrViewsets):
    #Manage Recipe in the Database
    queryset = Recipe.objects.all()
    serializer_class = serializers.RecipeSerializer

    def get_queryset(self):
        #Return Objects for the current authenticated user only
        return self.queryset.filter(user=self.request.user).order_by('-id')