from django.db import models

def get_or_create_simple_object(class_name: models.Model, **kwargs):
    if 'name' in kwargs:
        if kwargs['name'] == None:
            return None
    res, created = class_name.objects.get_or_create(**kwargs, defaults=kwargs)
    # try:
    #     res = class_name.objects.get(**kwargs)
    # except:
    #     res = class_name.objects.create(**kwargs)
    return res