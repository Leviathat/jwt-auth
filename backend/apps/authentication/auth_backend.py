from datetime import datetime

import jwt
from django.conf import settings
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed
from .models import User


class JWTAuthentication(authentication.BaseAuthentication):
    authentication_header_prefix = 'Bearer'

    def authenticate(self, request):
        auth_header = authentication.get_authorization_header(request).split()
        auth_header_prefix = self.authentication_header_prefix.lower()
        if not auth_header:
            return None

        if len(auth_header) == 1:
            return None

        elif len(auth_header) > 2:
            return None

        prefix = auth_header[0].decode('utf-8')
        token = auth_header[1].decode('utf-8')

        if prefix != self.authentication_header_prefix:
            return None

        return self._authenticate_credentials(request, token)

    def _authenticate_credentials(self, request, token):
        try:
            decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])

        except jwt.exceptions.DecodeError:
            raise AuthenticationFailed('Invalid token')

        expiration_time = datetime.utcfromtimestamp(decoded['exp'])
        current_time = datetime.utcnow()

        if current_time < expiration_time:
            raise AuthenticationFailed('Expired token')

        # МОГ БЫ СДЕЛАТЬ ТАК НАПИСАНО НИЖЕ, НО БЛЯТЬ PYJWT НЕ ХОЧЕТ СУКА КЛЮЧИ С ИСТЕКШИМ СРОКОМ ПРИЗАВАТЬ ЗА ИНВАЛИДОВ
        # except jwt.exceptions.ExpiredSignatureError:
        #     raise AuthenticationFailed('Expired token')

        try:
            user = User.objects.get(pk=decoded['id'])
        except User.DoesNotExist:
            msg = 'Пользователь соответствующий данному токену не найден.'
            raise AuthenticationFailed(msg)

        if not user.is_active:
            msg = 'Данный пользователь деактивирован.'
            raise AuthenticationFailed(msg)

        return (user, token)
