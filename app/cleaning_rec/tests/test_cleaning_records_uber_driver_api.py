from django.contrib.auth import get_user_model
from django.http import request
from rest_framework.reverse import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from core.models import UberDriver

UBERDRIVER_URL = reverse('cleaning_rec:driver-list')

def sample_uber_driver_record(driver_email):
    '''Create and return a sample uber driver record'''
    defaults = {
        'driver_first_name': 'Mallory',
        'driver_last_name': 'Cheryl',
    }

    return UberDriver.objects.create(driver_email=driver_email, **defaults)

class PublicUberDriverApiTests(TestCase):
    '''Tests unauthenticated Cleaning Records API access'''

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        '''Test that login is required'''
        res = self.client.get(UBERDRIVER_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateUberDriverApiTests(TestCase):
    '''Test the private cleaning records API'''
   
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'info@mallory.com',
            'fionamanny'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_create_valid_uber_driver_success(self):
        '''Test creating Uber Driver with valid payload is successful'''
        payload = {
            'driver_first_name': 'Mallory',
            'driver_last_name': 'Cheryl',
            'driver_email': 'info@mallory.com'
       }

        res = self.client.post(UBERDRIVER_URL, payload)
        self.assertAlmostEqual(res.status_code, status.HTTP_201_CREATED) 
        user = UberDriver.objects.get(**res.data)
        self.assertEqual(user.driver_email, payload['driver_email'])
        
    def test_uber_driver_exists(self):
        '''Test creating uber driver that already exists'''
        payload = {
            'driver_first_name': 'Mallory',
            'driver_last_name': 'Cheryl',
            'driver_email': 'info@mallory.com'
        }
        sample_uber_driver_record(payload['driver_email'])
        
        res = self.client.post(UBERDRIVER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)