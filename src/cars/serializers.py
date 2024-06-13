from rest_framework import serializers
from .models import *


class CarListSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='get_pretty_name')
    engine_type = serializers.CharField(source='engine_type.__str__')
    transmission_type = serializers.CharField(source='transmission_type.__str__')
    country_field = serializers.CharField(source='get_country.__str__')

    class Meta:
        model = Car
        fields = ['id', 'name', 'country_field', 'engine_capacity', 'engine_power', 'transmission_type', 'engine_type',
        'year_start', 'year_end', 'pict_url']


class CarDetailSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='get_pretty_name')
    engine_type = serializers.CharField(source='engine_type.__str__')
    transmission_type = serializers.CharField(source='transmission_type.__str__')
    body_type = serializers.CharField(source='body_type.__str__')
    drive_type = serializers.CharField(source='drive_type.__str__')
    country = serializers.CharField(source='get_country.__str__')
    
    class Meta:
        model = Car
        exclude = ['id', 'popularity', 'generation']
        # to_exclude = ['id', 'popularity', 'generation', 'favorites']
        # fields = ['country']

        # for field in Car._meta.get_fields():
        #     if field.name not in to_exclude:
        #         fields.append(field.name)


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        exclude = ['country']


class ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Model
        exclude = ['brand']


class GenerationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Generation
        exclude = ['model']


class BodyTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BodyType
        fields = '__all__'


class EngineTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngineType
        fields = '__all__'


class TransmissionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransmissionType
        fields = '__all__'


class DriveTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriveType
        fields = '__all__'

class TroubleSerializer(serializers.ModelSerializer):
    car = CarDetailSerializer()
    class Meta:
        model = Trouble
        fields = '__all__'

class ResolveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resolve
        fields = '__all__'

class MasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Master
        fields = '__all__'