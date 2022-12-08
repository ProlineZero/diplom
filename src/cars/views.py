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
@api_view(['POST'])
def add_car_to_database(request):
    try:
        req_dict = request.data
        
        country = get_or_create_simple_object(Country, name=req_dict['country'])

        brand = get_or_create_simple_object(Brand, name=req_dict['brand'], country=country)
        model = get_or_create_simple_object(Model, name=req_dict['model'], brand=brand)
        generation = get_or_create_simple_object(Generation, name=req_dict['generation'], model=model)

        engine_type = get_or_create_simple_object(EngineType, name=req_dict['engine_type'])
        transmission_type = get_or_create_simple_object(TransmissionType, name=req_dict['transmission_type'])
        body_type = get_or_create_simple_object(BodyType, name=req_dict['body_type'])
        
        get_or_create_simple_object(Car, generation=generation, engine_type=engine_type, 
        transmission_type=transmission_type, body_type=body_type, year_start=req_dict['year_begin'],
        year_end=req_dict['year_end'], engine_capacity=req_dict['engine_capacity'], 
        engine_power=req_dict['horse_power'], pict_id=req_dict['pict_name'])
    except:
        return HttpResponse('Автомобиль <span style="color: red;">не добавлен</span>! Проверьте правильность введенных данных и повторите попытку.')

    return HttpResponse('Автомобиль успешно <span style="color: green">добавлен!</span>')

# class CarManager(models.Manager):
#     def 

@api_view(['GET'])
def car_list(request):
    # try:
    #     if request.data['country']:
    #         country_id = Country.objects.get(name=request.data['country']).id
    #     else:
    #         country_id = -1

    #     if request.data['brand']:
    #         if country_id:
    #             brand_id = Brand.objects.get(country=country_id, name=request.data['brand']).id
    #         else:
    #             brand_id = Brand.objects.get(name=request.data['brand']).id

    #         if request.data['model']:
    #             model_id = Model.objects.get(brand=brand_id, name=request.data['model']).id
    #         generation_id = Generation.objects.get(model=model_id, name=request.data['generation']).id
    #     else:
    #         print()

    #     engine_type_id = EngineType.objects.get(name=request.data['engine_type']).id
    #     transmission_type_id = TransmissionType.objects.get(name=request.data['transmission_type']).id
    #     body_type_id = BodyType.objects.get(name=request.data['body_type']).id


    # except:
    #     return HttpResponse('говно запрос')

    cars_set = Car.objects.filter(get_model_id=10)

    serializer = CarListSerializer(cars_set, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def car_detail(request, id):
    cars = Car.objects.get(id=id)
    serializer = CarDetailSerializer(cars, many=False)
    return Response(serializer.data)

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