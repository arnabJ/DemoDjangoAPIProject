from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegistrationAPIView.as_view(), name='register'),  # Post
    path('login/', LoginAPIView.as_view(), name='login'),  # Post
    path('fetch_user_data/', FetchUserDataAPIView.as_view(), name="fetch_user_data"),  # Get
    path('update_user/<int:id>/', UpdateUserAPIView.as_view(), name="update_user"),  # Put

    path('address/<int:id>/', AddressAPIView.as_view(), name="address"),  # Get, Post, Put, Delete
    path('fetch_addresses/', FetchAddressesAPIView.as_view(), name="fetch_addresses"),  # Get
]
