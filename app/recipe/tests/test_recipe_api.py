from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Recipe
from recipe.serializers import RecipeSerializer

RECIPE_URL = reverse('recipe:recipe-list')

def sample_recipe(user, **params):
    #Create and return  a sample recipe
    defaults = {
        'title': 'Sample Recipe',
        'time_minutes': 10,
        'price': 5.00
    }
    defaults.update(params)

    return Recipe.objects.create(user=user, **defaults)

class PublicRecipeApiTests(TestCase):
    #Tests unauthenticated recipe API access

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        #Test that login is required
        res = self.client.get(RECIPE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateRecipeApiTests(TestCase):
    #Test the private ingredients API

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'info@mallory.com',
            'fionamanny'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_recipe(self):
        #Test retrieving the list of Recipes
        sample_recipe(user=self.user)
        sample_recipe(user=self.user)

        res = self.client.get(RECIPE_URL)

        recipes = Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)    

    def test_recipes_limited_to_user(self):
        #Test that Recipes returned are for the authenticated user
        user2 = get_user_model().objects.create_user(
            'info1@mallory.com',
            'fionamanny12'
        )
        sample_recipe(user2)
        sample_recipe(self.user)
        
        res = self.client.get(RECIPE_URL)
        recipes = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)

    '''def test_create_ingredient_successful(self):
        #Test creating a new Recipe
        payload = sample_recipe(self.user, {'title':'Chole'})
        self.client.post(RECIPE_URL, payload)

        exists = Recipe.objects.filter(
            user = self.user,
            name = payload['title']
        ).exists()

        self.assertTrue(exists)'''