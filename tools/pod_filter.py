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


def main():
    from delt.models import Pod
    pod =  Pod.objects.first()
    print(pod)
    print(pod.node.inputs)
    pods = Pod.objects.filter(node__inputs__contains=[{"identifier":"Representation"}]).filter(node__inputs__contains=[{"identifier":"ROI"}])
    print(pods)


if __name__ == "__main__":
    
    sys.path.insert(0, '/bergen')
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "arbeid.settings")
    django.setup()

    main()