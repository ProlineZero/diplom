from rest_framework import serializers
from .models import Car

class CarListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['name', 'engine_capacity', 'engine_power', 
        'transmission_type', 'engine_type', 'year_start', 'year_end']


class CarDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = '__all__'