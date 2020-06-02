from rest_framework import serializers

def modelToKwargs(serializer):
    kwargs = {}
    data = serializer.initial_data

    for f, field in serializer().fields.items():
        if not field.write_only:
            if isinstance(field, serializers.SerializerMethodField):
                kwargs[f] = field.to_representation(data)
            else:
                kwargs[f] = field.get_attribute(data)
            if f == "id":
                kwargs[f] = model.pk

    return kwargs

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