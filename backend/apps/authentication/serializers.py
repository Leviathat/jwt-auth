from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User


class RegistrationSerializer(serializers.ModelSerializer):
    """ Сериализация регистрации пользователя и создания нового. """

    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
    phone_number = serializers.CharField(
        max_length=11,
        min_length=11,
    )

    class Meta:
        model = User
        fields = ['email', 'phone_number', 'password', 'first_name', 'last_name']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):

    phone_number = serializers.CharField(
        max_length=11,
        min_length=11,
    )
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        phone_number = data.get('phone_number', None)
        password = data.get('password', None)

        if phone_number is None:
            raise serializers.ValidationError(
                'Номер телефона необходим для авторизации'
            )

        if password is None:
            raise serializers.ValidationError(
                'Пароль необходим для авторизации'
            )
        user = authenticate(username=phone_number, password=password)

        if user is None:
            raise serializers.ValidationError(
                'Пользователь с таким номером телефона или паролем не найден'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'Аккаунт заблокирован'
            )

        return {
            'email': user.email,
            'phone_number': user.phone_number,
            'token': user.token
        }


class UserSerializer(serializers.ModelSerializer):
    """ Сериализация и десериализация объектов User """

    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    class Meta:
        model = User
        fields = ['id', 'email', 'phone_number', 'password', 'first_name', 'last_name', 'token']
        read_only_fields = ('token', 'id')

    def update(self, instance, validated_data):
        """ Обновление User """

        password = validated_data.pop('password', None)

        for key, value in validated_data.items():
            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)

        instance.save()

        return instance
