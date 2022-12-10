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
    req_dict = request.data
    try:        
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
        Exceptions.objects.create(name=req_dict['id'])
        return HttpResponse('Автомобиль <span style="color: red;">не добавлен</span>! Проверьте правильность введенных данных и повторите попытку.')

    return HttpResponse('Автомобиль успешно <span style="color: green">добавлен!</span>')


@api_view(['GET'])
def car_list(request):
    cars = Car.objects.all()
    try:
        if request.data['country']:
            country_id = Country.objects.get(name=request.data['country']).id
        else:
            country_id = 0

        if request.data['brand']:
            if country_id:
                brand_id = Brand.objects.get(country=country_id, name=request.data['brand']).id
            else:
                brand_id = Brand.objects.get(name=request.data['brand']).id

            if request.data['model']:
                model_id = Model.objects.get(brand=brand_id, name=request.data['model']).id

                if request.data['generation']:
                    generation_id = Generation.objects.get(model=model_id, name=request.data['generation'])
                    cars = cars.filter(generation=generation_id)
                else: 
                    # выбрать все тачки где model - model_id
                    for car in cars:
                        if car.get_model_id() != model_id:
                            cars.exclude(car)
            else:
                # выбрать все тачки где brand - brand_id
                for car in cars:
                    if car.get_brand_id() != brand_id:
                        cars.exclude(car)
        else:
            if country_id:
                for car in cars:
                    if car.get_country_id() != country_id:
                        cars.exclude(car)


        engine_type_id = EngineType.objects.get(name=request.data['engine_type']).id
        transmission_type_id = TransmissionType.objects.get(name=request.data['transmission_type']).id
        body_type_id = BodyType.objects.get(name=request.data['body_type']).id
        drive_type_id = DriveType.objects.get(name=request.data['drive_type'])

        cars.filter(engine_type=engine_type_id, transmission_type=transmission_type_id,
        body_type=body_type_id, drive_type=drive_type_id, engine_capacity__gte=request.data['engine_capacity_from'],
        engine_capacity__lte=request.data['engine_capacity_to'],  engine_power__gte=request.data['engine_power_from'], 
        engine_power__lte=request.data['engine_power_to'], year_start_gte=request.data['year_start'],
        year_start_lte=request.data['year_end'])

        # if request.data['order_by']:
        #     cars.order_by(request.data['order_by'])
        # else:
        #     cars.order_by(popularity)


    except:
        return HttpResponse('говно запрос')

    serializer = CarListSerializer(cars, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def car_detail(request, id):
    car = Car.objects.get(id=id)
    car.popularity += 1
    car.save()

    serializer = CarDetailSerializer(car, many=False)
    return Response(serializer.data)