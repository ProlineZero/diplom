from django.urls import path
from .views import *

urlpatterns = [
    path('api/add/', add_car),
    path('api/start_parser/', add_car_to_database),
    
    path('api/get-countries/', get_countries),
    path('api/get-all-brands/', get_all_brands),
    path('api/get-brands/<int:country_id>/', get_brands),
    path('api/get-models/<int:brand_id>/', get_models),
    path('api/get-generations/<int:model_id>/', get_generations),

    path('api/get-all-body-types/', get_all_body_types),
    path('api/get-all-engine-types/', get_all_engine_types),
    path('api/get-all-transmission-types/', get_all_transmission_types),
    path('api/get-all-drive-types/', get_all_drive_types),

    path('api/get-engine-capacity-info/', get_engine_capacity_info),
    path('api/get-engine-power-info/', get_engine_power_info),
    path('api/get-year-start-info/', get_year_start_info),

    path('api/get-cars-list/', get_cars_list),
    path('api/cars-detail/<int:id>/', car_detail),

    path('api/register/', register_user),
    path('api/login/', login_user),
    path('api/add-to-favorites/', add_to_favorites),
    path('api/delete-from-favorites/', delete_from_favorites),
    path('api/get-favorites/', get_favorites),
    path('api/is-car-in-favorites/', is_car_in_favorites),

    path('api/become_master/', become_master),
    path('api/add_car_to_master/', add_car_to_master),
    path('api/get_masters_troubles/', get_masters_troubles),
    path('api/get_user_troubles/', get_user_troubles),
    path('api/get_trouble_resolves/', get_trouble_resolves),
    path('api/is_user_master/', is_user_master),
    path('api/add_resolve/', add_resolve),
    path('api/add_trouble/', add_trouble),
    path('api/get_car_troubles/', get_car_troubles),
    path('api/set_resolve_fight/', set_resolve_fight),
    path('api/get_master_data/', get_master_data),
]
