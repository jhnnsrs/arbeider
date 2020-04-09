# import the logging library
import json
import logging
# Get an instance of a logger
from uuid import uuid4

import django.db.models
import pandas as pd
import xarray as xr
import zarr as zr
from django.conf import settings
from django.db.models.manager import Manager
from django.db.models.query import QuerySet
from django.db import models
from xarray.backends import ZarrStore

from larvik.generators import ArnheimGenerator

logger = logging.getLogger(__name__)


class DelayedLarvikArrayManager(Manager):
    generatorClass = ArnheimGenerator
    group = None


    def from_xarray(self, array: xr.DataArray, fileversion=settings.LARVIK_FILEVERSION, apiversion= settings.LARVIK_APIVERSION,**kwargs ) -> (models.Model, ZarrStore):
        """Takes an DataArray and the model arguments and returns the created Model and the delayed Graph as ZarrStore
        
        Arguments:
            array {xr.DataArray} -- An xr.DataArray as a LarvikArray
        
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

        try: 
            df = array.biometa.channels.compute()
            channels = df.where(pd.notnull(df), None).to_dict('records')
            item.channels = channels
        except:
            logger.info("Representation does not Contain Channels?")
            


        # Actually Saving
        item.unique = uuid4()
        graph = item.store.save(array, compute=False, fileversion=fileversion, apiversion= apiversion)
        item.save()
        return (item, graph)


class LarvikArrayManager(Manager):
    generatorClass = ArnheimGenerator
    group = None


    def from_xarray(self, array: xr.DataArray, fileversion=settings.LARVIK_FILEVERSION, apiversion= settings.LARVIK_APIVERSION,**kwargs ):
        """Takes an DataArray and the model arguments and returns the created Model
        
        Arguments:
            array {xr.DataArray} -- An xr.DataArray as a LarvikArray
        
        Returns:
            [models.Model] -- [The Model]
        """
        import larvik.extenders as e

        item = self.model(**kwargs)
        generated = self.generatorClass(item, self.group)
        array.name = generated.name

        # Store Generation
        item.store.name = generated.path
        item.shape = list(array.shape)
        item.dims = list(array.dims)

        try: 
            df = array.biometa.channels.compute()
            channels = df.where(pd.notnull(df), None).to_dict('records')
            item.channels = channels
        except:
            logger.info("Representation does not Contain Channels?")
            


        # Actually Saving
        item.unique = uuid4()
        graph = item.store.save(array, compute=True,fileversion=fileversion, apiversion= apiversion)
        item.save()
        return item
