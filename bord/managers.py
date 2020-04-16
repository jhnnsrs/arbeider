# import the logging library
import logging
# Get an instance of a logger
from uuid import uuid4

from dask.dataframe import DataFrame
from django.conf import settings
from django.db.models.manager import Manager

from arbeid.settings import MATRISE_FILEVERSION
from bord.defaults import default_parquet_generator
from bord.querysets import BordQueryset

logger = logging.getLogger(__name__)


class DelayedBordManager(Manager):
    generatorClass = default_parquet_generator
    group = None
    queryset = None

    def get_queryset(self):
        if self.queryset is not None: return self.queryset(self.model, using=self._db)
        return BordQueryset(self.model, using=self._db)

    def from_dataframe(self, df: DataFrame, fileversion=settings.BORD_FILEVERSION, apiversion= settings.BORD_APIVERSION,**kwargs ):
        """Takes an DataFrame and the model arguments and returns the created Model and the delayed Graph as ZarrStore
        
        Arguments:
            array {xr.DataFrame} -- An xr.DataArray as a LarvikArray
        
        Returns:
            [models.Model] -- The Model
            [xarray.backends.ZarrStore] -- The Delayed Graph as a ParquetStore # TODO Wrong
        """
        item = self.model(**kwargs)
        generated = self.generatorClass(item, self.group)
        item.parquet.name = generated.path
            
        # Actually Saving
        item.unique = uuid4()
        graph = item.parquet.save(df, compute=False, fileversion=fileversion, apiversion= apiversion)
        item.save()
        return (item, graph)


class BordManager(Manager):
    generatorClass = default_parquet_generator
    group = None
    queryset = None
    
    def get_queryset(self):
        if self.queryset is not None: return self.queryset(self.model, using=self._db)
        return BordQueryset(self.model, using=self._db)


    def from_xarray(self, df: DataFrame, fileversion= settings.BORD_FILEVERSION, apiversion= settings.BORD_APIVERSION,**kwargs ):
        """Takes an DataFrame and the model arguments and returns the created Model
        
        Arguments:
            array {xr.DataArray} -- An xr.DataArray as a LarvikArray
        
        Returns:
            [models.Model] -- [The Model]
        """
        item = self.model(**kwargs)
        generated = self.generatorClass(item, self.group)
        item.parquet.name = generated.path

        # Actually Saving
        item.unique = uuid4()
        _ = item.parquet.save(df, compute=False, fileversion=fileversion, apiversion= apiversion)
        item.save()
        return item
