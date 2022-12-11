from rest_framework import serializers
from .models import Car, Country


class CarListSerializer(serializers.ModelSerializer):
    engine_type = serializers.CharField(source='engine_type.__str__')
    transmission_type = serializers.CharField(source='transmission_type.__str__')
    country_field = serializers.CharField(source='get_country.__str__')

    class Meta:
        model = Car
        fields = ['id', 'name', 'country_field', 'engine_capacity', 'engine_power', 'transmission_type', 'engine_type',
        'year_start', 'year_end', 'pict_url']


class CarDetailSerializer(serializers.ModelSerializer):
    engine_type = serializers.CharField(source='engine_type.__str__')
    transmission_type = serializers.CharField(source='transmission_type.__str__')
    body_type = serializers.CharField(source='body_type.__str__')
    drive_type = serializers.CharField(source='drive_type.__str__')
    # country_field = serializers.CharField(source='get_country.__str__')
    
    class Meta:
        model = Car
        # exclude = ['id', 'popularity', 'generation']
        fields = '__all__'


class CountryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'