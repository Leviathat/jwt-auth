from django.urls import path
from .views import RegistrationAPIView, LoginAPIView, UserRetrieveView

app_name = 'authentication'

urlpatterns = [
    path('register/', RegistrationAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('info/', UserRetrieveView.as_view())
]
