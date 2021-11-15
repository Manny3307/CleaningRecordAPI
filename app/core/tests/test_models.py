from django.test import TestCase
from django.contrib.auth import get_user_model

class MOdelTests(TestCase):

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
        self.assertTrue(user.is_admin)