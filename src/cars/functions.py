# from django.


def get_or_create_simple_object(class_name, **kwargs):
    try: 
        res = class_name.objects.get(**kwargs)
    except:
        res = class_name.objects.create(**kwargs)
    return res


# def testt(class_name, **kwargs):
#     return class_name.objects.get(**kwargs)