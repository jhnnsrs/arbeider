import json
import os
import sys

import dask.array as da
import django
import xarray as xr
import zarr as zr
from pandas.io.json import to_json
from rest_framework import serializers
from twisted.python.compat import xrange
from zarr.storage import DirectoryStore



def main():
    from delt.models import Provision
    from delt.serializers import ProvisionModelSerializer

    provision = Provision.objects.get(id=1)

    serialized = ProvisionModelSerializer(provision)
    data = serialized.data

    print(data)
    new = ProvisionModelSerializer(data=data)
    if new.is_valid(raise_exception=True):
        print(new.validated_data)
    

    ProvisionModelSerializer(new.validated_data)




if __name__ == "__main__":
    
    sys.path.insert(0, '/bergen')
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "arbeid.settings")
    django.setup()

    main()