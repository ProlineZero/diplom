from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, HttpResponseNotFound, Http404
from .models import *
from .functions import get_or_create_simple_object
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.
# class TestView(View):
#     def get(self, request):
#         request_dict = json.loads(request.body)
#         return HttpResponse(testt(Country, name='Japan').__str__())


#     def post(self, request):
#         return HttpResponse(request.POST["age"])

@csrf_exempt
def add_car_to_database(request):
    req_dict = json.loads(request.body)
    
    country = get_or_create_simple_object(Country, name=req_dict['country'])

    brand = get_or_create_simple_object(Brand, name=req_dict['brand'], country=country)
    model = get_or_create_simple_object(Model, name=req_dict['model'], brand=brand)
    generation = get_or_create_simple_object(Generation, name=req_dict['generation'], model=model)

    engine_type = get_or_create_simple_object(EngineType, name=req_dict['engine_type'])
    transmission_type = get_or_create_simple_object(TransmissionType, name=req_dict['transmission_type'])
    body_type = get_or_create_simple_object(BodyType, name=req_dict['body_type'])
    
    get_or_create_simple_object(Car, generation=generation, engine_type=engine_type, 
    transmission_type=transmission_type, body_type=body_type, production_start_year=req_dict['production_start_year'],
    engine_capacity=req_dict['engine_capacity'], engine_power=req_dict['engine_power'])
    return HttpResponse('Good')

# {
#     "country": "Germany",
#     "brand": "Mercedes-Benz",
#     "model": "E63 AMG",
#     "generation": "W212",
#     "engine_type": "Gasoline",
#     "transmission_type": "Automatic",
#     "body_type": "Sedan",
#     "engine_capacity": "5.5",
#     "engine_power": "585",
#     "production_start_year": "2013"
# }