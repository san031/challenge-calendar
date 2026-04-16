from django.urls import path,include
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

urlpatterns = [
    path('register/', RegisterAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('user-detail/',UserAPIView.as_view()),
    path('logout/', LogoutAPIView.as_view()),
    path('token/',TokenObtainPairView.as_view(),name='token_refresh'),
    path('token/refresh/',TokenObtainPairView.as_view(), name='token_refresh'),
]
