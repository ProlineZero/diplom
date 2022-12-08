from django.db import models
from django.db.models import Q, F
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
    name = models.CharField(max_length=100, blank=True)

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
    generation = models.ForeignKey(Generation, on_delete=models.PROTECT)
    engine_type = models.ForeignKey(EngineType, on_delete=models.PROTECT)
    transmission_type = models.ForeignKey(TransmissionType, on_delete=models.PROTECT)
    body_type = models.ForeignKey(BodyType, on_delete=models.PROTECT)
    engine_capacity = models.FloatField()
    engine_power = models.IntegerField()
    year_start = models.IntegerField()
    year_end = models.IntegerField(blank=True, null=True)
    popularity = models.IntegerField(default=0, blank=True)
    name = models.CharField(max_length=500, default='', blank=True)
    pict_id = models.IntegerField(default=0)

    class Meta:
        constraints = [
        models.CheckConstraint(check=(Q(year_start__gte=1850) & Q(year_start__lte=(datetime.date.today().year))), name='year_start'),
        models.CheckConstraint(check=(Q(year_end__gte=1850) & Q(year_end__lte=(datetime.date.today().year))), name='year_end'),
        models.CheckConstraint(check=(Q(engine_power__gt=0) & Q(engine_power__lte=5000)), name='engine_power'),
        models.CheckConstraint(check=(Q(engine_type=EngineType.objects.get(name='Электрический').id) | Q(engine_capacity__gte=0) & Q(engine_capacity__lte=30)), name='engine_capacity'),
    ]

    def save(self, *args, **kwargs):
        generation_str = Generation.objects.get(id=self.generation.id)
        model_str = Model.objects.get(id=generation_str.model.id)
        brand_str = Brand.objects.get(id=model_str.brand.id)
        self.name = brand_str.__str__() + ' ' + model_str.__str__() + ' ' + generation_str.__str__()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

    def get_model_id(self):
        return Generation.objects.get(id=self.generation.id).model.id

    def get_brand_id(self):
        return Model.objects.get(id=self.get_model_id()).brand.id

    def get_country_id(self):
        return Brand.objects.get(id=self.get_brand_id()).country.id
