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
        jwt_options = {
            'verify_signature': True,
            'verify_exp': True,
            'verify_nbf': False,
            'verify_iat': True,
            'verify_aud': False
        }
        
        try:    
            access_token = auth_data.decode('utf-8').split(' ')[1] 
            payload = jwt.decode(access_token,settings.SECRET_KEY,options=jwt_options,algorithms=['HS256'])      
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed(
                'Your token is expired, Please login again')
        except jwt.DecodeError as identifier:
            raise exceptions.AuthenticationFailed(
                'Your token is invalid,login')
        try:
            user = Author.objects.get(email=payload.get('email'))
            return (user, access_token)
        except Author.DoesNotExist:
            raise exceptions.AuthenticationFailed(
                'Not A Valid User Found'
            )      

        return super().authenticate(request)


class JWTAdminAuthentication(authentication.BaseAuthentication):
    authentication_header_prefix = 'Token'

    def authenticate(self, request):

        auth_data = authentication.get_authorization_header(request)

        if not auth_data:
            return None
        jwt_options = {
            'verify_signature': True,
            'verify_exp': True,
            'verify_nbf': False,
            'verify_iat': True,
            'verify_aud': False
        }
        
        try: 
            access_token = auth_data.decode('utf-8').split(' ')[1]    
            payload = jwt.decode(access_token,settings.SECRET_KEY,options=jwt_options,algorithms=['HS256'])
        except jwt.DecodeError as identifier:
            raise exceptions.AuthenticationFailed(
                'Your token is invalid,login')
        except jwt.ExpiredSignatureError as identifier:
            raise exceptions.AuthenticationFailed(
                'Your token is expired,login')
        try:   
            user = Admin.objects.get(email=payload.get('email'))
            return (user, access_token)
        except Admin.DoesNotExist:
            raise exceptions.AuthenticationFailed(
                'Not A Valid User Found'
            )
        return super().authenticate(request)