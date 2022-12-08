from rest_framework import serializers
from .models import Car


class CarListSerializer(serializers.ModelSerializer):
    engine_type = serializers.CharField(source='engine_type.__str__')
    transmission_type = serializers.CharField(source='transmission_type.__str__')

    class Meta:
        model = Car
        fields = ['id', 'name', 'engine_capacity', 'engine_power', 'transmission_type', 'engine_type',
        'year_start', 'year_end', 'pict_id']


class CarDetailSerializer(serializers.ModelSerializer):
    engine_type = serializers.CharField(source='engine_type.__str__')
    transmission_type = serializers.CharField(source='transmission_type.__str__')

    class Meta:
        model = Car
        fields = '__all__'