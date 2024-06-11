from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
import datetime

def my_str(self):
    if self.name == None:
        return ''
    return self.name

# Create your models here.
class Country(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        # return my_str(self)
        return self.name


class Brand(models.Model):
    country = models.ForeignKey(Country, on_delete=models.PROTECT)
    name = models.CharField(max_length=100)

    def __str__(self):
        return my_str(self)


class Model(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT)
    name = models.CharField(max_length=100)

    def __str__(self):
        return my_str(self)


class Generation(models.Model):
    model = models.ForeignKey(Model, on_delete=models.PROTECT)
    name = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return my_str(self)


class EngineType(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return my_str(self)


class TransmissionType(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return my_str(self)


class BodyType(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return my_str(self)


class DriveType(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return my_str(self)


class Car(models.Model):
    name = models.CharField(max_length=500, default='', blank=True)
    generation = models.ForeignKey(Generation, on_delete=models.PROTECT)
    
    engine_type = models.ForeignKey(EngineType, on_delete=models.PROTECT, null=True, blank=True)
    transmission_type = models.ForeignKey(TransmissionType, on_delete=models.PROTECT, null=True, blank=True)
    body_type = models.ForeignKey(BodyType, on_delete=models.PROTECT, null=True, blank=True)
    drive_type = models.ForeignKey(DriveType, on_delete=models.PROTECT, null=True, blank=True)
    popularity = models.IntegerField(default=0, null=True, blank=True)
    pict_url = models.CharField(max_length=200, null=True, blank=True)

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

    external_id = models.IntegerField(null=True, blank=True)

    class Meta:
        constraints = [
        models.CheckConstraint(check=(Q(year_start__gte=1850) & Q(year_start__lte=(datetime.date.today().year+1))), name='year_start'),
        models.CheckConstraint(check=(Q(year_end__gte=1850) & Q(year_end__lte=(datetime.date.today().year))), name='year_end'),
        models.CheckConstraint(check=(Q(engine_power__gt=0) & Q(engine_power__lte=5000)), name='engine_power'),
        # models.CheckConstraint(check=(Q(engine_type=EngineType.objects.get(name='Электро').id) | Q(engine_capacity__gte=0) & Q(engine_capacity__lte=30)), name='engine_capacity'),
    ]

    def save(self, *args, **kwargs):
        generation_str = Generation.objects.get(id=self.generation.id)
        model_str = Model.objects.get(id=generation_str.model.id)
        brand_str = Brand.objects.get(id=model_str.brand.id)
        self.name = brand_str.__str__().lower() + ' ' + model_str.__str__().lower() + ' ' + generation_str.__str__().lower()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return my_str(self)

    def get_model(self):
        return self.generation.model

    def get_brand(self):
        return self.generation.model.brand

    def get_country(self):
        return self.generation.model.brand.country

    def get_pretty_name(self):
        return (self.generation.model.brand.__str__()+' '+self.generation.model.__str__()+' '+self.generation.__str__())


class DBFiller(models.Model):
    external_id = models.IntegerField(null=True)
    added = models.IntegerField(null=True)


class Favorites(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    cars = models.ManyToManyField(Car)

class Compare(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    cars = models.ManyToManyField(Car)

class Master(models.Model):
    rating = models.IntegerField(db_column="rating", default=0)
    description = models.CharField(db_column="description", max_length=256, default="")

    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    cars = models.ManyToManyField(Car)

class Trouble(models.Model):
    description = models.CharField(db_column="description", max_length=256, default="")

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, db_column="car")

class Resolve(models.Model):
    description = models.CharField(db_column="description", max_length=256, default="")

    is_right = models.BooleanField(db_column="is_right", default=False)
    
    master = models.ForeignKey(Master, on_delete=models.CASCADE, null=True)
    trouble = models.ForeignKey(Trouble, on_delete=models.CASCADE, db_column="trouble")