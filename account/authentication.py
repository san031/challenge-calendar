from rest_framework import authentication,exceptions
from .models import User

import jwt
class JWTCookieAuthentication(authentication.BaseAuthentication):
    def authenticate(self,request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise exceptions.AuthenticationFailed("Unauthenticated !!")
        try:
            payload = jwt.decode(token,'secret',algorithms = ['HS256'])
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('unauthenticated!!')
        
        user = User.objects.filter(id = payload['id']).first()

        if user is None:
            raise exceptions.AuthenticationFailed("User not found")

        return (user,None)