from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Car)
admin.site.register(Country)
admin.site.register(Brand)
admin.site.register(Model)
admin.site.register(Generation)
admin.site.register(EngineType)
# admin.site.register(Transmission)
admin.site.register(BodyType)