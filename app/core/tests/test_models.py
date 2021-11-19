from datetime import time
from django.contrib.auth.models import User
from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models

def sample_user(email='info@mallory.com', password='fionamanny'):
    #Create a sample user
    return get_user_model().objects.create_user(email, password)

class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        #Test creating a new user with an email is successful

        email = "info@mallory.com"
        password = "fiona"
        user = get_user_model().objects.create_user(
            email = email,
            password = password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        #Test the email for the new user is normalized.
        email = 'test@MALLORY.COM'
        user = get_user_model().objects.create_user(email, 'test123')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        #Test crteating user with no email raises error.
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_create_new_superuser(self):
        #Test creating a new superuser.
        user = get_user_model().objects.create_superuser(
            'info@mallory.com',
            'fiona'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        #Test the tag string representation
        tag = models.Tag.objects.create(
            user = sample_user(),
            name = 'vegan'
        )

        self.assertEqual(str(tag), tag.name)
    
    def test_ingredient_str(self):
        #Test the ingredient strinhg representation
        ingredient = models.Ingredient.objects.create(
            user = sample_user(),
            name = 'cucumber'
        )

        self.assertEqual(str(ingredient), ingredient.name)

    def test_recipe_str(self):
        #Test the recipe string representation
        recipe = models.Recipe.objects.create(
            user = sample_user(),
            title = 'Steak and mushroon sauce',
            time_minutes = 5,
            price = 5.00
        )

        self.assertEqual(str(recipe), recipe.title)