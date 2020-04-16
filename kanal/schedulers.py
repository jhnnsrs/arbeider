from django.conf import settings

from dask import get as get_debug
from dask.distributed import Client
from dask.multiprocessing import get as get_multi
from dask.threaded import get as get_threaded


DEBUG = settings.DEBUG
DISTRIBUTED_CLIENT = None

DEFAULT_SCHEDULERS =  ["LOCAL","THREADED","MULTI","DISTRIBUTED"]




def get_default_scheduler(wanted = None):
    global get_debug, get_multi, get_threaded, DISTRIBUTED_CLIENT
    return get_threaded
    defaults = settings.ARNHEIM
    if defaults.dask_mode == "LOCAL" or wanted == "LOCAL":
        return get_debug
    if defaults.dask_mode == "THREADED" or wanted == "THREADED":
        return get_threaded
    if defaults.dask_mode == "MULTI" or wanted == "MULTI":
        return get_multi
    if defaults.dask_mode == "DISTRIBUTED" or wanted == "DISTRIBUTED":
        if DISTRIBUTED_CLIENT is None:
            DISTRIBUTED_CLIENT = Client(address= defaults.dask_scheduler_address)
        return DISTRIBUTED_CLIENT
