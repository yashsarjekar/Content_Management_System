import jwt
from django.conf import settings
from rest_framework import authentication, exceptions

from .models import Author, Admin


class JWTAuthorAuthentication(authentication.BaseAuthentication):
    authentication_header_prefix = 'Token'

    def authenticate(self, request):

        auth_data = authentication.get_authorization_header(request)

        if not auth_data:
            return None

        prefix, token = auth_data.decode('utf-8').split(' ')
        #print(token)
        payload = jwt.decode(token,options={"verify_signature": False})
        email = payload.get('email')
        #print(email)
        try:    
            user = Author.objects.get(email=payload.get('email'))
            return (user, token)
        except Author.DoesNotExist:
            raise exceptions.AuthenticationFailed(
                'Not A Valid User Found'
            )
        except jwt.DecodeError as identifier:
            raise exceptions.AuthenticationFailed(
                'Your token is invalid,login')
        except jwt.ExpiredSignatureError as identifier:
            raise exceptions.AuthenticationFailed(
                'Your token is expired,login')

        return super().authenticate(request)


class JWTAdminAuthentication(authentication.BaseAuthentication):
    authentication_header_prefix = 'Token'

    def authenticate(self, request):

        auth_data = authentication.get_authorization_header(request)

        if not auth_data:
            return None

        prefix, token = auth_data.decode('utf-8').split(' ')
        
        payload = jwt.decode(token,options={"verify_signature": False})
        email = payload.get('email')
        try:    
            user = Admin.objects.get(email=payload.get('email'))
            return (user, token)
        except Admin.DoesNotExist:
            raise exceptions.AuthenticationFailed(
                'Not A Valid User Found'
            )
        except jwt.DecodeError as identifier:
            raise exceptions.AuthenticationFailed(
                'Your token is invalid,login')
        except jwt.ExpiredSignatureError as identifier:
            raise exceptions.AuthenticationFailed(
                'Your token is expired,login')

        return super().authenticate(request)