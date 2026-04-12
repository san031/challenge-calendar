from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
# Create your models here.

class MyUserManager(BaseUserManager):
    def create_user(self,email,password = None, **extra_fields):
        if not email:
            raise ValueError("Email must be set")
        
        email = self.normalize_email(email)
        user = self.model(email = email, **extra_fields)
        # So This Line
        # pythonuser = self.model(email=email, **extra_fields)
        # Is exactly the same as writing:
        # pythonuser = MyUser(email=email, **extra_fields)
        user.set_password(password)
        user.save(using = self.db)   #same as user.save()
        return user


    def create_superuser(self,email,password=None,**extra_fields):
        extra_fields.setdefault("is_superuser",True)
        extra_fields.setdefault('is_staff',True)

        return self.create_user(email,password,**extra_fields)

class User(AbstractUser):
    email = models.EmailField(unique=True, max_length=255)
    full_name = models.CharField(max_length=100, default='')
    password = models.CharField(max_length=100)
    username = None

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []