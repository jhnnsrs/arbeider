from django.forms.models import model_to_dict
from rest_framework import serializers
from itertools import chain

def modelToKwargs(model, reverse_fields = []):
    opts = model._meta
    data = {}
    for f in chain(opts.concrete_fields, opts.private_fields):
        if f.is_relation:
            foreignkey = getattr(model, f.name)
            data[f.name] = foreignkey
            print(f"HERE {f.name}")
        else:
            data[f.name] = f.value_from_object(model)
        print(f"Setting {f.name}")
    for f in opts.many_to_many:
        data[f.name] = [i for i in f.value_from_object(model)]
    for f in reverse_fields:
        data[f] = getattr(model, f)

    return data

def modelToDict(model, exclude_fields=[]):
    opts = model._meta.get_fields()
    data = {}
    for f in opts:
        if f.name in exclude_fields: continue
        if f.one_to_many:
            print(f"{f.name} is many to one")
            data[f.name]= list(getattr(model, f.name).all())
        else:
            data[f.name]= getattr(model, f.name)

    return data

def serializerToDict(serializer):
    kwargs = {}
    data = serializer.initial_data
    print(serializer)
    for f, field in serializer.fields.items():
            if not field.write_only:
                if isinstance(field, serializers.SerializerMethodField):
                    kwargs[f] = field.to_representation(data[f])
                else:
                    try:
                        kwargs[f] = field.to_internal_value(data[f])
                    except:
                        try:
                            kwargs[f] = data[f]
                            continue
                        except:
                            continue

    return kwargs