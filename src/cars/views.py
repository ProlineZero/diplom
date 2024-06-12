from django.db.models import Q, F
from django.http import HttpResponse
from .models import *
from .functions import get_or_create_simple_object, _vol_if_key_exist
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *
from django.db.models import Min, Max
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
import jwt
import json

@api_view(['POST'])
def add_car(request):
    req_dict = dict(request.data.copy())
    response = {}
    try:        
        if not Car.objects.filter(external_id=req_dict['id']).exists():

            country = get_or_create_simple_object(Country, name=req_dict['country'])

            brand = get_or_create_simple_object(Brand, name=req_dict['brand'], country=country)
            model = get_or_create_simple_object(Model, name=req_dict['model'], brand=brand)
            generation = get_or_create_simple_object(Generation, name=req_dict['generation'], model=model)

            engine_type = get_or_create_simple_object(EngineType, name=req_dict['engine_type'])
            transmission_type = get_or_create_simple_object(TransmissionType, name=req_dict['transmission_type'])
            body_type = get_or_create_simple_object(BodyType, name=req_dict['body_type'])
            drive_type = get_or_create_simple_object(DriveType, name=req_dict['drive_type'])

            car = get_or_create_simple_object(
                Car, generation=generation, engine_type=engine_type, 
                transmission_type=transmission_type, body_type=body_type, drive_type=drive_type,
                year_start=req_dict['year_begin'],
                year_end=req_dict['year_end'], engine_capacity=req_dict['engine_capacity'], 
                engine_power=req_dict['horse_power'], pict_url=req_dict['pict_url'],
                body_length=req_dict['body_length'], body_width=req_dict['body_width'], body_height=req_dict['body_height'],
                kwt_power=req_dict['kwt_power'], weight=req_dict['weight'], seats=req_dict['seats'], 
                cylinders_order=req_dict['cylinders_order'], cylinders_number=req_dict['cylinders_value'], torque=req_dict['torque'], 
                max_speed=req_dict['max_speed'], time_to_100=req_dict['time_to_100'], front_brakes=req_dict['front_brakes'],
                back_brakes=req_dict['back_brakes']
                )

            if car:
                car.external_id = req_dict['id']
                car.save()

            response = CarDetailSerializer(car).data
        else:
            response["message"] = f"Автомобиль уже был добавлен"
        # return Response(f"Ошибка {e}: {e.__class__} - {e.__context__}")
    except Exception as e:
        response = f"Ошибка {e}: {e.__class__} - {e.__context__}"

    return Response(response)

@csrf_exempt
@api_view(['GET'])
def add_car_to_database(request):
    url = 'http://193.124.33.120/'
    pictUrl = 'resources/pictures/'
    with open("baseN.json", "r", encoding="utf8") as dataFile:
        raw_data = json.loads(dataFile.read())

        for brand in raw_data :
            brand_name = brand["name"]
            country = brand["country"]

            for model in brand["models"] :
                model_name = model["name"]
                
                for gen in model["generations"] :
                    gen_name = gen["name"]
                    year_begin = gen["year-start"]
                    year_end = gen["year-stop"]
                    
                    for config in gen["configurations"] :
                        pict_name = config["id"]
                        body_type = config["body-type"]
                        
                        for modification in config["modifications"] :
                            id = str(int(modification["complectation-id"]) + 1)
                            if int(id) != 59127 and int(id) != 79180 and int(id) != 79181 and int(id) != 79182:
                                continue
                            else:
                                print()
                            engine_type = _vol_if_key_exist("engine-type", modification["specifications"])
                            transmission_type = _vol_if_key_exist("transmission", modification["specifications"])
                            horse_power = _vol_if_key_exist("horse-power", modification["specifications"])
                            kwt_power = _vol_if_key_exist("kvt-power", modification["specifications"])
                            engine_capacity = _vol_if_key_exist("volume-litres", modification["specifications"])
                            torque = _vol_if_key_exist("moment", modification["specifications"])
                            drive = _vol_if_key_exist("drive", modification["specifications"])
                            cylinders_order = _vol_if_key_exist("cylinders-order", modification["specifications"])
                            cylinders_value = _vol_if_key_exist("cylinders-value", modification["specifications"])
                            body_length = _vol_if_key_exist("length", modification["specifications"])
                            body_width = _vol_if_key_exist("width", modification["specifications"])
                            body_height = _vol_if_key_exist("height", modification["specifications"])
                            front_brake = _vol_if_key_exist("front-brake", modification["specifications"])
                            back_brake = _vol_if_key_exist("back-brake", modification["specifications"])
                            if len(modification["specifications"]["seats"]) > 1 :
                                seats = modification["specifications"]["seats"][1]
                            else :
                                seats = modification["specifications"]["seats"][0]
                            weight = _vol_if_key_exist("weight", modification["specifications"])
                            max_speed = _vol_if_key_exist("max-speed", modification["specifications"])
                            time_to_100 = _vol_if_key_exist("time-to-100", modification["specifications"])
                            
                            req_dict = {
                                'id': id,
                                'country': country,
                                'brand': brand_name,
                                'model': model_name,
                                'generation': gen_name,
                                'year_begin': year_begin,
                                'year_end': year_end,
                                'body_type': str(body_type).title() if body_type else body_type,
                                'body_length': body_length,
                                'body_width': body_width,
                                'body_height': body_height,
                                'weight': weight,
                                'seats': seats,
                                'pict_url': f'{url}{pictUrl}{pict_name}.jpg',
                                'engine_type': str(engine_type).title() if engine_type else engine_type,
                                'transmission_type': str(transmission_type).title() if transmission_type else transmission_type,
                                'drive_type': str(drive).title() if drive else drive,
                                'engine_capacity': engine_capacity,
                                'cylinders_order': str(cylinders_order).title() if cylinders_order else cylinders_order,
                                'cylinders_value': cylinders_value,
                                'horse_power': horse_power,
                                'kwt_power': kwt_power,
                                'torque': torque,
                                'max_speed': max_speed,
                                'time_to_100': time_to_100,
                                'front_brakes': str(front_brake).title() if front_brake else front_brake,
                                'back_brakes': str(back_brake).title() if back_brake else back_brake
                            }
                            try:        
                                if not Car.objects.filter(external_id=req_dict['id']).exists():
                                    fillerRecord = DBFiller(external_id=req_dict['id'])

                                    country = get_or_create_simple_object(Country, name=req_dict['country'])

                                    brand = get_or_create_simple_object(Brand, name=req_dict['brand'], country=country)
                                    model = get_or_create_simple_object(Model, name=req_dict['model'], brand=brand)
                                    generation = get_or_create_simple_object(Generation, name=req_dict['generation'], model=model)

                                    engine_type = get_or_create_simple_object(EngineType, name=req_dict['engine_type'])
                                    transmission_type = get_or_create_simple_object(TransmissionType, name=req_dict['transmission_type'])
                                    body_type = get_or_create_simple_object(BodyType, name=req_dict['body_type'])
                                    drive_type = get_or_create_simple_object(DriveType, name=req_dict['drive_type'])

                                    car = get_or_create_simple_object(Car, generation=generation, engine_type=engine_type, 
                                    transmission_type=transmission_type, body_type=body_type, drive_type=drive_type,
                                    year_start=req_dict['year_begin'],
                                    year_end=req_dict['year_end'], engine_capacity=req_dict['engine_capacity'], 
                                    engine_power=req_dict['horse_power'], pict_url=req_dict['pict_url'],
                                    body_length=req_dict['body_length'], body_width=req_dict['body_width'], body_height=req_dict['body_height'],
                                    kwt_power=req_dict['kwt_power'], weight=req_dict['weight'], seats=req_dict['seats'], 
                                    cylinders_order=req_dict['cylinders_order'], cylinders_number=req_dict['cylinders_value'], torque=req_dict['torque'], 
                                    max_speed=req_dict['max_speed'], time_to_100=req_dict['time_to_100'], front_brakes=req_dict['front_brakes'],
                                    back_brakes=req_dict['back_brakes'])

                                    if car:
                                        car.external_id = req_dict['id']
                                        car.save()
                                        fillerRecord.added = 1
                                    else:
                                        fillerRecord.added = 0
                                    
                                    fillerRecord.save()
                            except Exception as e:
                                fillerRecord.added = -100
                                fillerRecord.save()

    return HttpResponse('Операция проведена')


def get_all_cars_in_generations_filtered(generations, **filters):
    cars = Car.objects.none()
    for generation in generations:
        cars |= generation.car_set.filter(**filters)

    return cars


def get_all_generations_in_models(models):
    generations = Generation.objects.none()
    for model in models:
        generations |= model.generation_set.all()

    return generations


def get_all_models_in_brands(brands):
    models = Model.objects.none()
    for brand in brands:
        models |= brand.model_set.all()

    return models


@api_view(['POST'])
def get_cars_list(request):
    try:
        filters = {}

        if 'name' in request.data:
            filters['name__icontains'] = request.data['name']

        if 'engine_type' in request.data:
            filters['engine_type'] = request.data['engine_type']

        if 'transmission_type' in request.data:
            filters['transmission_type'] = request.data['transmission_type']

        if 'body_type' in request.data:
            filters['body_type'] = request.data['body_type']

        if 'drive_type' in request.data:
            filters['drive_type'] = request.data['drive_type']

        if 'engine_capacity_from' in request.data:
            filters['engine_capacity__gte'] = request.data['engine_capacity_from']
        
        if 'engine_capacity_to' in request.data:
            filters['engine_capacity__lte'] = request.data['engine_capacity_to']

        if 'engine_power_from' in request.data:
            filters['engine_power__gte'] = request.data['engine_power_from']

        if 'engine_power_to' in request.data:
            filters['engine_power__lte'] = request.data['engine_power_to']

        if 'year_start_from' in request.data:
            filters['year_start__gte'] = request.data['year_start_from']

        if 'year_start_to' in request.data:
            filters['year_start__lte'] = request.data['year_start_to']

        if 'generation' in request.data:
            cars = Car.objects.filter(generation=request.data['generation'], **filters)
        elif 'model' in request.data:
            generations = Generation.objects.filter(model=request.data['model'])
            cars = get_all_cars_in_generations_filtered(generations, **filters)
        elif 'brand' in request.data:
            models = Model.objects.filter(brand=request.data['brand'])
            generations = get_all_generations_in_models(models)
            cars = get_all_cars_in_generations_filtered(generations, **filters)
        elif 'country' in request.data:
            brands = Brand.objects.filter(country=request.data['country'])
            models = get_all_models_in_brands(brands)
            generations = get_all_generations_in_models(models)
            cars = get_all_cars_in_generations_filtered(generations, **filters)
        else:
            cars = Car.objects.filter(**filters)

        if 'order_by' in request.data:
            # cars = cars.order_by(F(request.data['order_by']).desc(nulls_last=True))
            cars = cars.order_by(request.data['order_by'])
        else:
            cars = cars.order_by('-popularity')

        if 'offset' in request.data and 'limit' in request.data:
            cars = cars[request.data['offset']:request.data['offset']+request.data['limit']]

        serializer = CarListSerializer(cars, many=True)

        return Response(serializer.data)
    except  Exception as e:
        return HttpResponse(f"По вашему запросу ничего не найдено: {e}: {e.__context__}")


@api_view(['GET'])
def car_detail(request, id):
    response = {}
    try:
        print(f"WTF")
        car = Car.objects.get(id=id)
        car.popularity += 1
        car.save()

        serializer = CarDetailSerializer(car, many=False)
        response = serializer.data
    except ObjectDoesNotExist:
        response = {f"Автомобиль не найден"}
    except Exception as e:
        response = {f"except Exception: {e}: {e.__class__} {e.__context__}"}

    return Response(response)


# API for filters info
@api_view(['GET'])
def get_countries(requset):
    countries = Country.objects.order_by('name')

    serializer = CountrySerializer(countries, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_all_brands(request):
    brands = Brand.objects.all().order_by('name')

    serializer = BrandSerializer(brands, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_brands(request, country_id):
    brands = Brand.objects.filter(country=country_id).order_by('name')

    serializer = BrandSerializer(brands, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_models(request, brand_id):
    models = Model.objects.filter(brand=brand_id).order_by('name')

    serializer = ModelSerializer(models, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_generations(request, model_id):
    generations = Generation.objects.filter(model=model_id).order_by('name')

    serializer = GenerationSerializer(generations, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_all_body_types(reqiest):
    body_types = BodyType.objects.all().order_by('name')

    serializer = BodyTypeSerializer(body_types, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_all_engine_types(reqiest):
    engine_types = EngineType.objects.all().order_by('name')

    serializer = EngineTypeSerializer(engine_types, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_all_transmission_types(reqiest):
    transmission_types = TransmissionType.objects.all().order_by('name')

    serializer = TransmissionTypeSerializer(transmission_types, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_all_drive_types(reqiest):
    drive_types = DriveType.objects.all().order_by('name')

    serializer = DriveTypeSerializer(drive_types, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_engine_capacity_info(request):

    return Response(Car.objects.aggregate(min=Min('engine_capacity'), max=Max('engine_capacity')))


@api_view(['GET'])
def get_engine_power_info(request):

    return Response(Car.objects.aggregate(min=Min('engine_power'), max=Max('engine_power')))


@api_view(['GET'])
def get_year_start_info(request):
    
    return Response(Car.objects.aggregate(min=Min('year_start'), max=Max('year_start')))


jwt_encoder = "ms73mb937twp1mv6"
@api_view(['POST'])
def register_user(request):
    
    success = False
    try:
        user = User.objects.create_user(request.data['email'], request.data['email'], request.data['password'])
        encoded_jwt = jwt.encode({"email": request.data['email']}, jwt_encoder, algorithm="HS256")
        if 'first_name' in request.data:
            user.first_name = request.data['first_name']
        if 'last_name' in request.data:
            user.last_name = request.data['last_name']
        user.save()
        success = True
        return Response({"success": success, "jwt": encoded_jwt})
    except Exception as e:
        print(f"Except error {e}: {e.__class__} - {e.__context__}")
        success = False
        return Response({"success": f"Except error {e}: {e.__class__} - {e.__context__}"})


@api_view(['POST'])
def login_user(request):

    user = authenticate(username=request.data['email'], password=request.data['password'])
    if user:
        encoded_jwt = jwt.encode({"email": request.data['email']}, jwt_encoder, algorithm="HS256")
        return Response({"jwt": encoded_jwt})
    else:
        return HttpResponse('Unauthorized', status=401)


@api_view(['POST'])
def add_to_favorites(request):
    try:
        decoded_jwt = jwt.decode(request.headers["Authorization"].replace("Bearer", "").replace(" ", ""), jwt_encoder, algorithms=["HS256"])
        user = User.objects.get(email=decoded_jwt['email'])
        car_id = request.data['car_id']

        get_or_create_simple_object(Favorites, user=user)
        try:
            user = Favorites.objects.get(user=user)
        except:
            user = Favorites.objects.create(user=user)
        user.cars.add(car_id)
    except:
        return Response('bad request')

    return Response('good request')


@api_view(['POST'])
def delete_from_favorites(request):
    try:
        decoded_jwt = jwt.decode(request.headers["Authorization"].replace("Bearer", "").replace(" ", ""), jwt_encoder, algorithms=["HS256"])
        user = User.objects.get(email=decoded_jwt['email'])
        car_id = request.data['car_id']

        user = Favorites.objects.get(user=user)
        user.cars.get(id=car_id).delete()
    except:
        return Response('bad request')

    return Response('good request')


@api_view(['POST'])
def get_favorites(request):
    try:
        decoded_jwt = jwt.decode(request.headers["Authorization"].replace("Bearer", "").replace(" ", ""), jwt_encoder, algorithms=["HS256"])
        user = User.objects.get(email=decoded_jwt['email'])
        user = Favorites.objects.get(user=user)

        cars = user.cars.all().order_by("-popularity")
        serializer = CarListSerializer(cars, many=True)
        return Response(serializer.data)
    except:
        return Response('bad request', status=400)


@api_view(['POST'])
def become_master(request):
    try:
        decoded_jwt = jwt.decode(request.headers["Authorization"].replace("Bearer", "").replace(" ", ""), jwt_encoder, algorithms=["HS256"])
        user = User.objects.get(email=decoded_jwt['email'])
        master_data = {
            "user_id": user
        }
        master = Master.objects.create(**master_data)
        serializer = MasterSerializer(master)
        return Response(serializer.data)
    except Exception as e:
        print(f"Except error {e}: {e.__class__} - {e.__context__}")
        return HttpResponse('bad request')
    
@api_view(['GET'])
def get_master_data(request):
    try:
        decoded_jwt = jwt.decode(request.headers["Authorization"].replace("Bearer", "").replace(" ", ""), jwt_encoder, algorithms=["HS256"])
        user = User.objects.get(email=decoded_jwt['email'])
        master = Master.objects.get(user_id=user.id)
        
        serializer = MasterSerializer(master)
        return Response(serializer.data)
    except Exception as e:
        print(f"Except error {e}: {e.__class__} - {e.__context__}")
        return HttpResponse('bad request')


@api_view(['POST'])
def add_car_to_master(request):
    try:
        car = request.data.get("car", None)
        decoded_jwt = jwt.decode(request.headers["Authorization"].replace("Bearer", "").replace(" ", ""), jwt_encoder, algorithms=["HS256"])
        user = User.objects.get(email=decoded_jwt['email'])
        
        master = Master.objects.get(user_id=user.id)

        master.cars.add(car)

        serializer = MasterSerializer(master)
        return Response(serializer.data)
    except Exception as e:
        print(f"Except error {e}: {e.__class__} - {e.__context__}")
        return HttpResponse('bad request')

@api_view(['POST'])
def add_trouble(request):
    try:
        car = request.data.get("car", None)
        name = request.data.get("name", None)
        description = request.data.get("description", None)
        decoded_jwt = jwt.decode(request.headers["Authorization"].replace("Bearer", "").replace(" ", ""), jwt_encoder, algorithms=["HS256"])
        user = User.objects.get(email=decoded_jwt['email'])
        
        car = Car.objects.get(id=car)
        trouble_data = {
            "name": name,
            "description": description,

            "car": car,
            "user": user,
        }

        trouble = Trouble.objects.create(**trouble_data)

        serializer = TroubleSerializer(trouble)

        return Response(serializer.data)
    except Exception as e:
        print(f"Except error {e}: {e.__class__} - {e.__context__}")
        return HttpResponse('bad request')

@api_view(['POST'])
def add_resolve(request):
    try:
        decoded_jwt = jwt.decode(request.headers["Authorization"].replace("Bearer", "").replace(" ", ""), jwt_encoder, algorithms=["HS256"])

        description = request.data.get("description", None)
        trouble = request.data.get("trouble", None)
        

        user = User.objects.get(email=decoded_jwt['email'])
        master = Master.objects.get(user_id=user.id)
        trouble = Trouble.objects.get(id=trouble)

        resolve_data = {
            "description": description,

            "master": master,
            "trouble": trouble,
        }

        resolve = Resolve.objects.create(**resolve_data)

        serializer = ResolveSerializer(resolve)

        return Response(serializer.data)
    except Exception as e:
        print(f"Except error {e}: {e.__class__} - {e.__context__}")
        return HttpResponse('bad request')


@api_view(['GET'])
def get_masters_troubles(request):
    try:
        decoded_jwt = jwt.decode(request.headers["Authorization"].replace("Bearer", "").replace(" ", ""), jwt_encoder, algorithms=["HS256"])
        user = User.objects.get(email=decoded_jwt['email'])
        
        master = Master.objects.get(user_id=user.id)

        troubles = Trouble.objects.filter(resolved=False, car__in=master.cars.all().values_list("id", flat=True)).order_by("-id")
        serializer = TroubleSerializer(troubles, many=True)

        return Response(serializer.data)
    except:
        HttpResponse('bad request')

    return Response('good request')

@api_view(['POST'])
def set_resolve_fight(request):
    try:
        decoded_jwt = jwt.decode(request.headers["Authorization"].replace("Bearer", "").replace(" ", ""), jwt_encoder, algorithms=["HS256"])
        user = User.objects.get(email=decoded_jwt['email'])
        resolve_id = request.data.get("resolve", None)

        resolve = Resolve.objects.get(id=resolve_id)
        resolve.is_right = True
        trouble = resolve.trouble
        trouble.resolved = True
        trouble.save()

        master = resolve.master
        master.rating += 1
        master.save()
        
        serializer = ResolveSerializer(resolve)

        return Response(serializer.data)
    except:
        HttpResponse('bad request')

    return Response('good request')

@api_view(['GET'])
def get_user_troubles(request):
    try:
        decoded_jwt = jwt.decode(request.headers["Authorization"].replace("Bearer", "").replace(" ", ""), jwt_encoder, algorithms=["HS256"])
        user = User.objects.get(email=decoded_jwt['email'])

        troubles = user.troubles.all().order_by("-id")
        serializer = TroubleSerializer(troubles, many=True)
        return Response(serializer.data)
    except:
        HttpResponse('bad request')

    return Response('good request')

@api_view(['GET'])
def get_car_troubles(request):
    try:
        decoded_jwt = jwt.decode(request.headers["Authorization"].replace("Bearer", "").replace(" ", ""), jwt_encoder, algorithms=["HS256"])
        user = User.objects.get(email=decoded_jwt['email'])
        car = request.GET.get("car", None)

        troubles = Trouble.objects.filter(car=car).order_by("-id")

        serializer = TroubleSerializer(troubles, many=True)
        return Response(serializer.data)
    except:
        HttpResponse('bad request')

    return Response('good request')

@api_view(['GET'])
def get_trouble_resolves(request):
    try:
        trouble = request.GET.get("trouble", None)

        resolves = Resolve.objects.filter(trouble=trouble).order_by("-id")
        serializer = ResolveSerializer(resolves, many=True)
        return Response(serializer.data)
    except:
        HttpResponse('bad request')

    return Response('good request')


@api_view(['POST'])
def is_car_in_favorites(request):
    try:
        decoded_jwt = jwt.decode(request.headers["Authorization"].replace("Bearer", "").replace(" ", ""), jwt_encoder, algorithms=["HS256"])
        user = User.objects.get(email=decoded_jwt['email'])
        car_id = request.data['car_id']

        user = Favorites.objects.get(user=user)
        try:
            user.cars.get(id=car_id)
            res = True
        except:
            res = False
    except:
        HttpResponse('bad request')

    return Response({"success": res})

@api_view(['GET'])
def is_user_master(request):
    try:
        decoded_jwt = jwt.decode(request.headers["Authorization"].replace("Bearer", "").replace(" ", ""), jwt_encoder, algorithms=["HS256"])
        user = User.objects.get(email=decoded_jwt['email'])
        if Master.objects.filter(user_id=user.id).exists():
            res = True
        else:
            res = False
    except Exception as e:
        print(f"Except error {e}: {e.__class__} - {e.__context__}")

        HttpResponse('bad request')

    return Response({"success": res})

