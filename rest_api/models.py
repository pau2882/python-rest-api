from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager


class UserProfileManager(BaseUserManager):
    """Manager for user profile"""

    def create_user(self, email, name, password=None):
        """Create a new user profile"""
        if not email:
            raise ValueError('User must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, name=name)

        'make sure the password is stored as hash, encrypted'
        user.set_password(password)

        'saving django object in the database'
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password):
        """Create and save a new superuser with with a given details.
        self is automatically passed in when the function is being called."""
        user = self.create_user(email, name, password)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Database model for users in the system"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    """replacing the default USERNAME_FIELD from AbstractBaseUser to email (ie.
    instead of username, we would like an email)"""
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    'for django to interact with our custom model'
    'defining a function within a class, self must be used as the argument'
    def get_full_name(self):
        """Retrieve full name of user"""
        return self.name


    def get_short_name(self):
        """Retrieve short name of user"""
        return self.name

    def __str__(self):
        """Return string representation of the model.  Recommanded for
        Django app"""
        return self.email
