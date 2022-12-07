from django.urls import path
from .views import *

urlpatterns = [
    path('api/adddss/', add_car_to_database),
    path('api/test/', api_test),
    path('api/cars-list/', car_list),
    path('api/cars-detail/<int:id>/', car_detail),
]
