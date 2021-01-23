import datetime
import jwt
from django.conf import settings

def generate_access_token(user):
    data = {
        'email': user.email,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=2),
        'iat': datetime.datetime.utcnow(),
    }
    access_token = jwt.encode(data,
                              settings.SECRET_KEY)
    return access_token


def generate_refresh_token(user):
    data = {
        'email': user.email,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
        'iat': datetime.datetime.utcnow(),
    }
    refresh_token = jwt.encode(data,
                              settings.REFRESH_TOKEN_SECRET_KEY)
    return refresh_token