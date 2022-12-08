from django.urls import path
from .views import *

urlpatterns = [
    path('api/add/', add_car_to_database),
    path('api/cars-list/', car_list),
    path('api/cars-detail/<int:id>/', car_detail),
]
