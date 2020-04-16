# import the logging library
import json
import logging
# Get an instance of a logger
from uuid import uuid4

import xarray as xr
from django.conf import settings
from django.db.models.manager import Manager
from xarray.backends import ZarrStore

from matrise.defaults import default_zarr_generator
from matrise.querysets import MatriseQueryset

logger = logging.getLogger(__name__)


class DelayedMatriseManager(Manager):
    generatorClass = default_zarr_generator
    group = None
    queryset = None

    def get_queryset(self):
        if self.queryset is not None: return self.queryset(self.model, using=self._db)
        return MatriseQueryset(self.model, using=self._db)


    def from_xarray(self, array: xr.DataArray, fileversion=settings.MATRISE_FILEVERSION, apiversion= settings.MATRISE_APIVERSION,**kwargs ):
        """Takes an DataArray and the model arguments and returns the created Model and the delayed Graph as ZarrStore
        
        Arguments:
            array {xr.DataArray} -- An xr.DataArray as a Matrise
        
        Returns:
            [models.Model] -- The Model
            [xarray.backends.ZarrStore] -- The Delayed Graph as a ZarrStore
        """
        item = self.model(**kwargs)
        generated = self.generatorClass(item, self.group)
        array.name = generated.name

        # Store Generation
        item.store.name = generated.path
        item.shape = list(array.shape)
        item.dims = list(array.dims)

        # Actually Saving
        item.unique = uuid4()
        graph = item.store.save(array, compute=False, fileversion=fileversion, apiversion= apiversion)
        item.save()
        return (item, graph)


class MatriseManager(Manager):
    generatorClass = default_zarr_generator
    group = None
    queryset = None

    def get_queryset(self):
        if self.queryset is not None: return self.queryset(self.model, using=self._db)
        return MatriseQueryset(self.model, using=self._db)

    def from_xarray(self, array: xr.DataArray, fileversion=settings.MATRISE_FILEVERSION, apiversion= settings.MATRISE_APIVERSION,**kwargs ):
        """Takes an DataArray and the model arguments and returns the created Model
        
        Arguments:
            array {xr.DataArray} -- An xr.DataArray as a LarvikArray
        
        Returns:
            [models.Model] -- [The Model]
        """

        item = self.model(**kwargs)
        generated = self.generatorClass(item, self.group)
        array.name = generated.name

        # Store Generation
        item.store.name = generated.path
        item.shape = list(array.shape)
        item.dims = list(array.dims)        


        # Actually Saving
        item.unique = uuid4()
        graph = item.store.save(array, compute=True,fileversion=fileversion, apiversion= apiversion)
        item.save()
        return item
