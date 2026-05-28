from django.shortcuts import render
from rest_framework import views,permissions
from rest_framework.response import Response
from .serializers import UserSerializer
from .models import User
from rest_framework.exceptions import AuthenticationFailed
import jwt
import datetime
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
    def post(self,request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email = email).first()

        if user is None:
            raise AuthenticationFailed("user not found")
        
        if not user.check_password(password):
            raise AuthenticationFailed("Invalid password")

        payload = {
            "id" : user.id,
            "email" : user.email,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            "iat": datetime.datetime.utcnow()

        }

        # jwt has 3 parts separated by dots: Header.payload.signature

        #header --> token type and algorithm used
        #payload --> actual data: {user id, email id}
        #signature --> proves the token has not been tampered with
        token = jwt.encode(payload,'secret',algorithm='HS256')

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)

        response.data = {
            'jwttoken' : token
        }

        return response
    


class UserAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    # authentication_classes = [JWTCookieAuthentication]

    def get(self,request):
        

        serializer = UserSerializer(request.user)
        print(f"user-detail data: {request.user}  , serializer:{serializer}")

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


class jwtToken(views.APIView):
    permission_classes=[permissions.AllowAny]
    authentication_classes = [JWTCookieAuthentication]

    def get(self,request):
        token = request.COOKIES.get('jwt')

        return Response({'token': token})
