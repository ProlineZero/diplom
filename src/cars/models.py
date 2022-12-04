from django.db import models

# Create your models here.
class Country(models.Model):
    name = models.CharField(max_length=100)


class Brand(models.Model):
    country_id = models.ForeignKey(Country, on_delete=models.PROTECT)
    name = models.CharField(max_length=100)


class Model(models.Model):
    brand_id = models.ForeignKey(Brand, on_delete=models.PROTECT)
    name = models.CharField(max_length=100)


class Generation(models.Model):
    model_id = models.ForeignKey(Model, on_delete=models.PROTECT)
    name = models.CharField(max_length=100)


class EngineType(models.Model):
    name = models.CharField(max_length=100)


class Transmission(models.Model):
    name = models.CharField(max_length=100)


class Transmission(models.Model):
    name = models.CharField(max_length=100)


class BodyType(models.Model):
    name = models.CharField(max_length=100)


class Car(models.Model):
    engine_type_id = models.ForeignKey(EngineType, on_delete=models.PROTECT)
    transmission_id = models.ForeignKey(Transmission, on_delete=models.PROTECT)
    body_type_id = models.ForeignKey(BodyType, on_delete=models.PROTECT)
    generation_id = models.ForeignKey(Generation, on_delete=models.PROTECT)
    production_start_year = models.IntegerField()
    engine_capacity = models.FloatField()
    engine_power = models.IntegerField()
    popularity = models.IntegerField()