from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.
class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None):
        # Ensure the user has an email address
        if not email:
            raise ValueError('User must have an email address')
        
        # Ensure the user has a username
        if not username:
            raise ValueError('User must have an username')

        user = self.model(
            email=self.normalize_email(email),  # Normalize the email before saving
            username=username,
            first_name=first_name,
            last_name=last_name
        )

        user.set_password(password)  # Set the password properly (hashed)
        user.save(using=self._db)  # Save the user instance to the database
        return user

    def create_superuser(self, first_name, last_name, username, email, password):
        # Create the superuser with the required attributes
        user = self.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=self.normalize_email(email),
            password=password
        )
        # Set superuser-specific flags
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser):
    # Define the fields for the custom user model
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=50, blank=True, null=True)

    # Required fields
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)

    # Boolean fields for user roles
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)  # Set to True by default
    is_superadmin = models.BooleanField(default=False)

    # Specify which field will be used to authenticate users (email in this case)
    USERNAME_FIELD = 'email'
    
    # Other required fields for creating a user
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']

    # Custom manager to handle user creation
    objects = MyAccountManager()

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_admin  # Check if the user has admin privileges
    
    def has_module_perms(self, add_label):
        return True  # Return True to allow access to modules

