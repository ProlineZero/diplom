from django.db import models
from django.db.models import Q
import datetime

# Create your models here.
class Country(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Brand(models.Model):
    country = models.ForeignKey(Country, on_delete=models.PROTECT)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Model(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Generation(models.Model):
    model = models.ForeignKey(Model, on_delete=models.PROTECT)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class EngineType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class TransmissionType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class BodyType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Car(models.Model):
    engine_type = models.ForeignKey(EngineType, on_delete=models.PROTECT)
    transmission_type = models.ForeignKey(TransmissionType, on_delete=models.PROTECT)
    body_type = models.ForeignKey(BodyType, on_delete=models.PROTECT)
    generation = models.ForeignKey(Generation, on_delete=models.PROTECT)
    production_start_year = models.IntegerField()
    engine_capacity = models.FloatField()
    engine_power = models.IntegerField()
    popularity = models.IntegerField(default=0, blank=True)

    class Meta:
        constraints = [
        models.CheckConstraint(check=(Q(production_start_year__gte=1850) & Q(production_start_year__lte=(datetime.date.today().year))), name='production_start_year'),
        models.CheckConstraint(check=(Q(engine_power__gt=0) & Q(engine_power__lte=5000)), name='engine_power'),
        models.CheckConstraint(check=(Q(engine_type=EngineType.objects.get(name='Electric').id) | Q(engine_capacity__gte=0) & Q(engine_capacity__lte=30)), name='engine_capacity'),
    ]

    def __str__(self):
        generation_str = Generation.objects.get(id=self.generation.id)
        model_str = Model.objects.get(id=generation_str.model.id)
        brand_str = Brand.objects.get(id=model_str.brand.id)
        return brand_str.__str__() + ' ' + model_str.__str__() + ' ' + generation_str.__str__()