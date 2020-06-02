import json
import os
import sys

import dask.array as da
import django
import xarray as xr
import zarr as zr
from pandas.io.json import to_json
from twisted.python.compat import xrange
from zarr.storage import DirectoryStore

from rest_framework import serializers


def main():
    from elements.models import Representation, Sample
    from elements.serializers import RepresentationSerializer

    rep = Representation.objects.get(id=1)

    serialized = RepresentationSerializer(rep)
    data = serialized.data

    print(data)
    new = RepresentationSerializer(data=data)
    kwargs = {}
    data = new.initial_data

    for f, field in new.fields.items():
        if not field.write_only:
            if isinstance(field, serializers.SerializerMethodField):
                kwargs[f] = field.to_representation(data[f])
            else:
                try:
                    kwargs[f] = field.to_internal_value(data[f])
                except:
                    kwargs[f] = data[f]
                    continue

    print(kwargs)



if __name__ == "__main__":
    
    sys.path.insert(0, '/bergen')
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "arbeid.settings")
    django.setup()

    main()