
from django.conf import settings
from django.utils.functional import LazyObject
from django.utils.module_loading import import_string
from django.conf import settings 

from arbeid.settings import MATRISE_FILEVERSION


def get_default_zarr_storage(import_path=None):
    return import_string(import_path or settings.DEFAULT_ZARR_STORAGE)


class DefaultZarrStorage(LazyObject):
    def _setup(self):
        self._wrapped = get_default_zarr_storage()()


default_zarr_storage = DefaultZarrStorage()


def get_default_zarr_generator(import_path=None):
    return import_string(import_path or settings.DEFAULT_ZARR_GENERATOR or settings.DEFAULT_NAME_GENERATOR)


class DefaultZarrGenerator(LazyObject):
    def _setup(self, *args, **kwargs):
        self._wrapped = get_default_zarr_generator()(*args, **kwargs)


default_zarr_generator = DefaultZarrGenerator

def get_default_file_version():
    try:
        return settings.MATRISE_FILEVERSION
    except AttributeError as e:
        return "beta"
