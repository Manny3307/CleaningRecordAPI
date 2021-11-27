from django.contrib.auth import get_user_model
from django.http import request
from rest_framework.reverse import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from core.models import UberDriver
