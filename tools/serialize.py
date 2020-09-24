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
from itertools import chain

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



def main():
    from delt.models import Provision

    provision = Provision.objects.get(id=738)

    dictio = modelToKwargs(provision)
    print(dictio)



if __name__ == "__main__":
    
    sys.path.insert(0, '/bergen')
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "arbeid.settings")
    django.setup()

    main()