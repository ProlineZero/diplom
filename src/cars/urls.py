from django.urls import path
from .views import *

urlpatterns = [
    path('api/adddss/', add_car_to_database)
]
