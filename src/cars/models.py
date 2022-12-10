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


class DriveType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Car(models.Model):
    name = models.CharField(max_length=500, default='', blank=True)
    generation = models.ForeignKey(Generation, on_delete=models.PROTECT)
    
    engine_type = models.ForeignKey(EngineType, on_delete=models.PROTECT, null=True, blank=True)
    transmission_type = models.ForeignKey(TransmissionType, on_delete=models.PROTECT, null=True, blank=True)
    body_type = models.ForeignKey(BodyType, on_delete=models.PROTECT, null=True, blank=True)
    drive_type = models.ForeignKey(DriveType, on_delete=models.PROTECT, null=True, blank=True)
    popularity = models.IntegerField(default=0, null=True, blank=True)
    pict_id = models.IntegerField(default=0, null=True, blank=True)

    engine_capacity = models.FloatField(null=True, blank=True)
    engine_power = models.IntegerField(null=True, blank=True)
    kwt_power = models.IntegerField(null=True, blank=True)
    year_start = models.IntegerField(null=True, blank=True)
    year_end = models.IntegerField(blank=True, null=True)
    body_length = models.IntegerField(null=True, blank=True)
    body_width = models.IntegerField(null=True, blank=True)
    body_height = models.IntegerField(null=True, blank=True)
    weight = models.IntegerField(null=True, blank=True)
    seats = models.IntegerField(null=True, blank=True)
    cylinders_order = models.CharField(max_length=100, null=True, blank=True)
    cylinders_number = models.IntegerField(null=True, blank=True)
    torque = models.IntegerField(null=True, blank=True)
    max_speed = models.IntegerField(null=True, blank=True)
    time_to_100 = models.FloatField(null=True, blank=True)
    front_brakes = models.CharField(max_length=100, null=True, blank=True)
    back_brakes = models.CharField(max_length=100, null=True, blank=True)

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


class Exceptions(models.Model):
    name = models.CharField(max_length=100, null=True)


# {
#     "country": "Германия",
#     "brand": "Mercedes-Benz",
#     "model": "E63 AMG",
#     "generation": "W212",
#     "engine_type": "Бензин",
#     "transmission_type": "Роботизированная",
#     "body_type": "Седан",
#     "engine_capacity": "5.5",
#     "engine_power": "585",
#     "year_start": "2013",
#     "year_end": "2018",
#     "pict_id": "123123"
# }