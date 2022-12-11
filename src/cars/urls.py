from django.urls import path
from .views import *

urlpatterns = [
    path('api/add/', add_car_to_database),
    path('api/cars-list/', car_list),
    path('api/cars-detail/<int:id>/', car_detail),
    path('api/get-countries/', get_countries),
    # path('api/get-brands/<int:country_id>/', get_brands),
    # path('api/get-models/<int:brand_id>/', get_models),
    # path('api/get-generations/<int:model_id>/', get_generations),


    path('api/sergay-loh/', get_random_cars)
]
