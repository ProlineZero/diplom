from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, HttpResponseNotFound, Http404
from .models import *
from .functions import get_or_create_simple_object
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import CarListSerializer, CarDetailSerializer
import json

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
    transmission_type=transmission_type, body_type=body_type, year_start=req_dict['year_start'],
    year_end=req_dict['year_end'],engine_capacity=req_dict['engine_capacity'], 
    engine_power=req_dict['engine_power'], pict_id=req_dict['pict_id'])

    return HttpResponse('Good')


@api_view(['GET'])
def api_test(request):
    api_urls = {
        'aboba': 'yes',
        'not aboba': 'bo'
    }

    return Response(api_urls)


@api_view(['GET'])
def car_list(reqest):
    cars = Car.objects.all()
    serializer = CarListSerializer(cars, many=True)
    return Response(serializer.data )


@api_view(['GET'])
def car_detail(reqest, id):
    cars = Car.objects.get(id=id)
    serializer = CarDetailSerializer(cars, many=False)
    return Response(serializer.data )

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
#     "year_start": "2013",
#     "year_end": "2018",
#     "pict_id": "123123"
# }