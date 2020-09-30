# import the logging library
import json
import logging

from django.core.files.uploadedfile import InMemoryUploadedFile
from matrise.helpers import array_to_image
from matrise.extenders import ArnheimError
from matrise.mixins import AutoGenerateImageFromArrayMixin, WithChannel, WithPlanes
# Get an instance of a logger
from uuid import uuid4
from channels.db import database_sync_to_async
import xarray as xr
from django.conf import settings
from django.db.models.manager import Manager
from xarray.backends import ZarrStore
import numpy as np
from matrise.defaults import default_zarr_generator
from matrise.querysets import MatriseQueryset
import io

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
      


        if isinstance(item,WithChannel):
            try:
                channels = array.biometa.channels.compute().replace({np.nan:None})
                channels.columns = map(str.lower, channels.columns)
                item.channels = channels.to_dict(orient="records")
            except ArnheimError as e:
                logger.info(e)

        if isinstance(item,WithPlanes):
            try:
                planes = array.biometa.planes.compute().replace({np.nan:None})
                planes.columns = map(str.lower, planes.columns)
                item.planes = planes.to_dict(orient="records")
            except ArnheimError as e:
                logger.info(e)

        if isinstance(item, AutoGenerateImageFromArrayMixin):
            img = array_to_image(array, rescale=item._meta.rescale, max= item._meta.max, slicefunction = item._meta.slicefunction)
            
            img_io = io.BytesIO()
            img.save(img_io, format='jpeg', quality=100)
            image = InMemoryUploadedFile(img_io, None, self.name + ".jpeg", 'image/jpeg',
                                                img_io.tell, None)

            
            item.image = image

        item.save()
        return item
