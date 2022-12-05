from django.db import models
from django.db.models import Q
import datetime

# Create your models here.
class Country(models.Model):
    name = models.CharField(max_length=100)


class Brand(models.Model):
    country = models.ForeignKey(Country, on_delete=models.PROTECT)
    name = models.CharField(max_length=100)


class Model(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT)
    name = models.CharField(max_length=100)


class Generation(models.Model):
    model = models.ForeignKey(Model, on_delete=models.PROTECT)
    name = models.CharField(max_length=100)


class EngineType(models.Model):
    name = models.CharField(max_length=100)


# class Transmission(models.Model):
#     name = models.CharField(max_length=100)


class BodyType(models.Model):
    name = models.CharField(max_length=100)


class Car(models.Model):
    engine_type = models.ForeignKey(EngineType, on_delete=models.PROTECT)
    # transmission_type = models.ForeignKey(TransmissionType, on_delete=models.PROTECT)
    body_type = models.ForeignKey(BodyType, on_delete=models.PROTECT)
    generation = models.ForeignKey(Generation, on_delete=models.PROTECT)
    production_start_year = models.IntegerField()
    engine_capacity = models.FloatField()
    engine_power = models.IntegerField()
    popularity = models.IntegerField()

    class Meta:
        constraints = [
        models.CheckConstraint(check=(Q(production_start_year__gte=1850) & Q(production_start_year__lte=(datetime.date.today().year))), name='production_start_year'),
        models.CheckConstraint(check=(Q(engine_power__gt=0) & Q(engine_power__lte=5000)), name='engine_power'),
        models.CheckConstraint(check=(Q(engine_capacity__gte=0) & Q(engine_capacity__lte=30)), name='engine_capacity'),
    ]