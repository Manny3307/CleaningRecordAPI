from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')

def create_user(**params):
    return get_user_model().objects.create_user(**params)

class PublicUserApiTests(TestCase):
    '''Test the users API public'''

    def setUp(self):
        self.client = APIClient()

    def test_createvalid_user_success(self):
        '''Test creating user with valid payload is successful'''
        payload = {
            'email': 'info@mallory.com',
            'password': 'fiona',
            'name': 'Mallory Cheryl',
            'Middle_Name': 'Cheryl',
            'Last_Name': 'Branford',
            'User_Mobile': '0416438047',
            'Landline_Number': '',
            'Driver_Address': 'learmonth drive, monee ponds',
            'Driver_License': '0123456789',
            'Driver_CPVV_Certificate': 'DC123456',
            'Driver_Car_Rego': '1JU5NC',
            'Driver_Car_VIN': 'MR053REH205284934',
            'Driver_Car_Insurance_Provider': 'Real Insurance',
            'Driver_Car_Insurance_Cover': 'Comprehensive'
       }

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertAlmostEqual(res.status_code, status.HTTP_201_CREATED) 
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        '''Test creating user that already exists'''
        payload = {
            'email': 'info@mallory.com',
            'password': 'fiona',
            'name': 'Mallory Cheryl'
        }
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        '''Test if the Password is shorter than 5 Characters'''
        payload = {
            'email': 'info@mallory.com',
            'password': 'fi',
            'name': 'Mallory Cheryl'
        }
        
        res = self.client.post(CREATE_USER_URL, payload)
        
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        
        user_exists = get_user_model().objects.filter(
            email = payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        '''Test that token is created by the User'''
        payload = {
            'email': 'info@mallory.com',
            'password': 'fi'
        }
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        '''Test that token is not created if invalid credentials are given'''
        create_user(email="info@mallory.com", password="fiona")
        payload = {'email': 'info@mallory.com', 'password': 'Manny'}

        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data) 
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        '''Test that token is not created if user doesn't exists'''
        payload = {'email': 'info@mallory.com', 'password': 'fiona'}

        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data) 
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        '''Test that email and password are required'''
        payload = {'email': 'test', 'password': ''}

        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data) 
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorised(self):
        '''Test that authentication is required for users'''

        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateUserApiTest(TestCase):
    '''Test API requests that require Authentication'''

    def setUp(self):
        self.user = create_user(
            email='info@mallory.com',
            password='fionamanny',
            name='Mallory'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        '''Test retireving profile for logged in user'''

        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'name': self.user.name,
            'email': self.user.email,
            'Middle_Name': self.user.Middle_Name,
            'Last_Name': self.user.Last_Name,
            'User_Mobile': self.user.User_Mobile,
            'Landline_Number': self.user.Landline_Number,
            'Driver_Address': self.user.Driver_Address,
            'Driver_License': self.user.Driver_License,
            'Driver_CPVV_Certificate': self.user.Driver_CPVV_Certificate,
            'Driver_Car_Rego': self.user.Driver_Car_Rego,
            'Driver_Car_VIN': self.user.Driver_Car_VIN,
            'Driver_Car_Insurance_Provider': self.user.Driver_Car_Insurance_Provider,
            'Driver_Car_Insurance_Cover': self.user.Driver_Car_Insurance_Cover
        })

    def test_post_me_not_allowed(self):
        '''Test that POST is not allowed on me url'''

        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        '''Test updating the user profile for authenticated user'''
        payload = {
            'name': 'info@mallory.com',
            'password': 'fionamanny'
        }

        res = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)