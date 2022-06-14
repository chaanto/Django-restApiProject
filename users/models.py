from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from templatetags.gravatars import gravatar

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, password, is_staff=False, is_superuser=False):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.is_staff = is_staff
        user.is_superuser = is_superuser
        user.save()
        return user

    def create_staffuser(self, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
            is_staff = True,
            is_superuser = False
        )
        user.staff = True
        user.save()
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
            is_staff = True,
            is_superuser = True
        )
        
        user.save()
        return user


class User(AbstractUser):
    name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    profile_picture = models.ImageField(blank=True, default=gravatar(email))
    
    
    
    username = None
    objects= UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

