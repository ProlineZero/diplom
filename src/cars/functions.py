# from django.


def get_or_create_simple_object(class_name, **kwargs):
    if 'name' in kwargs:
        if kwargs['name'] == None:
            return None
    try:
        res = class_name.objects.get(**kwargs)
    except:
        res = class_name.objects.create(**kwargs)
    return res