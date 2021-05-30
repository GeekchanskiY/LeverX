from django.db import models
from django.conf import settings

from django.contrib.auth.models import AbstractUser

import jwt

from datetime import datetime, timedelta

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
        return self.username

    @property
    def token(self):
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        """
        Генерирует веб-токен JSON, в котором хранится идентификатор этого
        пользователя, срок действия токена составляет 1 день от создания
        """
        dt = datetime.now() + timedelta(days=1)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%S'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"