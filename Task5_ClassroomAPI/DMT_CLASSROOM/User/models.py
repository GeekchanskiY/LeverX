from django.db import models
from django.contrib.auth.models import AbstractUser

# Можно было бы и AbstractBaseUser тут забацать, но в данном случае и этого хватает вроде как

class User(AbstractUser):
    email = models.EmailField(max_length=150, unique=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255)
    is_staff = models.BooleanField(default=False)


    user_status_choices = [
        ("S", "Student"),
        ("T", "Teacher")
    ]
    user_status = models.CharField(max_length=1, choices=user_status_choices, default="S")

    REQUIRED_FIELDS = ['user_status', 'password', 'username']
    USERNAME_FIELD = 'email'

    def __str__(self):
        return email