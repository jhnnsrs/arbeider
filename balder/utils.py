from django.forms.models import model_to_dict
from rest_framework import serializers
from itertools import chain



def modelToDict(model, exclude_fields=[]):
    opts = model._meta.get_fields()
    data = {}
    for f in opts:
        if f.name in exclude_fields: continue
        if f.one_to_many:
            data[f.name]= list(getattr(model, f.name).all())
        else:
            # check if "ID is set from serialize" and change to pk:
            field = f.name  #if f.name != "id" else "pk"
            data[field]= getattr(model, f.name)

    return data

def serializerToDict(serializer):
    kwargs = {}
    data = serializer.initial_data
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