from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
    
    def create_user(self, email, password=None, **extra_fields):
        #Creates and saves a new user
        if not email:
            raise ValueError('User must enter an email address')

        user = self.model(email= self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        #Creates and saves a new Super User.
        user = self.create_user(email, password)
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)

        return user

class User(AbstractBaseUser, PermissionsMixin):
    #Custom user model that supports using email instead of username.

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    #last_name = models.CharField(max_length=255)
    '''user_mobile = models.CharField(max_length=15, Required=True)
    user_landline = models.CharField(max_length=15)
    user_address = models.CharField(max_length=500, Required=True)
    user_license = models.IntegerField(max_length=10, Required=True)
    user_CPVV_certificate = models.CharField(max_length=15, Required=True)
    user_car_rego = models.CharField(max_length=10, Required = True)
    user_car_VIN = models.CharField(max_length=50, Required = True)
    user_car_insurance_provider = models.CharField(max_length=250, Required = True)
    user_car_insurance_cover = models.CharField(max_length=250, Required = True)
'''
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'