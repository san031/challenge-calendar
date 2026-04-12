from django.urls import path,include
from .views import *

urlpatterns = [
    path('register/', RegisterAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('user-detail/',UserAPIView.as_view()),
    path('logout/', LogoutAPIView.as_view())
]
