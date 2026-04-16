from django.shortcuts import render
from rest_framework import views,permissions
from rest_framework.response import Response
from .serializers import UserSerializer
from .models import User
from rest_framework.exceptions import AuthenticationFailed
import jwt
from .authentication import JWTCookieAuthentication
# Create your views here.

class RegisterAPIView(views.APIView):
    permission_classes = [permissions.AllowAny]
    def post(self,request):
        serializer = UserSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
class LoginAPIView(views.APIView):
    permission_classes = [permissions.AllowAny]
    def post(Self,request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email = email).first()

        if user is None:
            raise AuthenticationFailed("user not found")
        
        if not user.check_password(password):
            raise AuthenticationFailed("Invalid password")

        payload = {
            "id" : user.id,
            "email" : user.email
        }

        # jwt has 3 parts separated by dots: Header.payload.signature

        #header --> token type and algorithm used
        #payload --> actual data: {user id, email id}
        #signature --> proves the token has not been tampered with
        token = jwt.encode(payload,'secret',algorithm='HS256')

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)

        response.data = {
            'jwt token' : token
        }

        return response
    


class UserAPIView(views.APIView):
    permission_classes = [permissions.AllowAny]
    def get(self,request):
        token = request.COOKIES.get('jwt')
        print(token)
        #reading the JWT token from the browser's cookies

        if not token:
            raise AuthenticationFailed("Unauthenticated!!")
         
        try:
            payload = jwt.decode(token,'secret', algorithms=['HS256'])
            # The payload will store whatever data you put into JWT when it was created
            print(payload)
            #Decode token → get user id from payload → fetch user from database

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!!')
        
        # here payload is used after decoding
        user = User.objects.filter(id = payload['id']).first()

        serializer = UserSerializer(user)

        return Response(serializer.data)


class LogoutAPIView(views.APIView):
    authentication_classes = [JWTCookieAuthentication]

    permission_classes = [permissions.AllowAny]
    def post(self,request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message' : "successful"
        }
        return response
