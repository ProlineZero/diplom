from django.db import models

def _vol_if_key_exist(key, dict) :
    if key in dict :
        return dict[key]
    else :
        return None

def get_or_create_simple_object(class_name: models.Model, **kwargs):
    if 'name' in kwargs:
        if kwargs['name'] == None:
            return None
    res, created = class_name.objects.get_or_create(**kwargs, defaults=kwargs)

    return res