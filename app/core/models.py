from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
import uuid
import os

from django.db.models.base import Model
from django.db.models.deletion import CASCADE

def recipe_image_file_path(instance, filename):
    """Generate file path for new recipe image"""
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('uploads/recipe/', filename)


class UserManager(BaseUserManager):
    
    def create_user(self, email, password=None, **extra_fields):
        '''Creates and saves a new user'''
        if not email:
            raise ValueError('User must enter an email address')

        user = self.model(email= self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        '''Creates and saves a new Super User.'''
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user

class User(AbstractBaseUser, PermissionsMixin):
    '''Custom user model that supports using email instead of username.'''

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Tag(models.Model):
    '''Tag to be used for the recipe'''
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name

class Ingredient(models.Model):
    '''Ingredient to be used in a recipe'''
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class Recipe(models.Model):
    '''Recipe Object'''
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.CharField(max_length=255, blank=True)
    ingredients = models.ManyToManyField('Ingredient')
    tags = models.ManyToManyField('Tag')
    image = models.ImageField(null=True, upload_to=recipe_image_file_path)
    
    def __str__(self):
        return self.title

###########################################
# Driver Cleaning Records API Section     #
###########################################

class UberDriver(models.Model):
    '''Driver details Object'''
    driver_id = models.AutoField(primary_key=True)
    driver_email = models.EmailField(max_length=200, unique=True)
    driver_first_name = models.CharField(max_length=500)
    driver_last_name = models.CharField(max_length=500, blank=True)


class UberDriverContactInfo(models.Model):
    '''Driver Contact Info Object'''
    driver_contact_id = models.AutoField(primary_key=True)
    driver_id = models.ForeignKey(UberDriver, on_delete=CASCADE)
    driver_contact_type = models.CharField(max_length=20)
    driver_contact_value = models.CharField(max_length=1000)

   
class UberRegisteredCar(models.Model):
    '''Driver Car details Object'''
    uber_car_id = models.AutoField(primary_key=True)
    uber_car_rego = models.CharField(max_length=15)
    uber_car_vin = models.CharField(max_length=100)
    uber_car_insurance_provider = models.CharField(max_length=150)
    uber_car_insurance_type = models.CharField(max_length=50)

class UberTempCleaningRecords(models.Model):
    '''Driver Temporary Cleaning Records Object'''
    Date_and_time_of_trip = models.TextField()
    Date_and_Time_of_clean = models.TextField()
    Driver_name = models.TextField()
    Driver_email = models.EmailField(max_length=200, unique=True)
    Driver_certificate_number = models.TextField()
    Passenger_hightouch_surfaces_cleaned = models.TextField()
    Driver_hightouch_surfaces_cleaned = models.TextField()

class UberDriverCPVVCertificate(models.Model):
    '''Driver CPVV Certificate Details Object'''
    driver_certificate_id = models.AutoField(primary_key=True)
    driver_id = models.ForeignKey(UberDriver, on_delete=CASCADE)
    driver_cpvv_certicate = models.CharField(max_length=25)

class UberCleaningRecords(models.Model):
    '''Driver Cleaning Records Object'''
    driver_id = models.ForeignKey(UberDriver, on_delete=CASCADE)
    driver_certificate_id = models.ForeignKey(UberDriverCPVVCertificate, on_delete=CASCADE)
    date_and_time_of_trip = models.DateTimeField()
    date_and_time_of_clean = models.DateTimeField()
    passenger_high_touch_surfaces = models.CharField(max_length=5)
    driver_high_touch_surfaces = models.CharField(max_length=5)


class UberDriverCar(models.Model):
    '''Driver Car Relationship Object'''
    driver_id = models.ForeignKey(UberDriver, on_delete=CASCADE)
    uber_car_id = models.ForeignKey(UberRegisteredCar, on_delete=CASCADE)


class UberDriverTripRecord(models.Model):
    '''Driver Trip Record Object'''
    driver_id = models.ForeignKey(UberDriver, on_delete=models.CASCADE)
    driver_phone_number = models.CharField(max_length=15)
    driver_email = models.CharField(max_length=50)
    driver_trip_id = models.CharField(max_length=50)
    driver_trip_type = models.CharField(max_length=15)
    driver_trip_base_fare = models.CharField(max_length=5)
    driver_trip_cancellation_fare = models.CharField(max_length=5, blank=True)
    driver_trip_date_time = models.CharField(max_length=45)
    driver_trip_fare_min_or_supplement = models.CharField(max_length=5, blank=True)
    driver_trip_fare_supplement = models.CharField(max_length=5, blank=True)
    driver_trip_wait_time = models.CharField(max_length=5, blank=True)
    driver_trip_service_fee = models.CharField(max_length=5, blank=True)
    driver_trip_tip = models.CharField(max_length=5, blank=True)
    driver_trip_total = models.CharField(max_length=10)