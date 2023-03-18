from datetime import timedelta, datetime

import jwt
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone
from django.conf import settings


class UserManager(BaseUserManager):
    def create_user(self, phone_number, first_name, last_name, password=None, email=None):
        if phone_number is None:
            raise TypeError('Users must have a username.')
        user = self.model(phone_number=phone_number, first_name=first_name, last_name=last_name, email=email)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, phone_number, first_name, last_name, password):
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(phone_number, 'admin', 'admin', password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser):
    email = models.EmailField(unique=True, null=True, default=None)
    phone_number = models.CharField(db_index=True, max_length=11, unique=True)
    first_name = models.CharField(max_length=40, blank=True)
    last_name = models.CharField(max_length=40, blank=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        return f'{self.last_name} {self.first_name}'

    @property
    def token(self):
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        """
        Генерация JWT токена с указанным user_id и expiration date через 7 дней
        """

        # Установка даты истечения токена через 7 дней
        exp = datetime.now() + timedelta(seconds=5)

        # Установка параметров заголовка токена
        headers = {'typ': 'jwt', 'alg': 'HS256'}

        # Создание словаря данных токена (payload)
        payload = {
            'id': self.pk,
            'exp': exp
        }

        # Генерация токена с помощью PyJWT
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256', headers=headers)

        # Возвращаем токен в виде строки
        return token
