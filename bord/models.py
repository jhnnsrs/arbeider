# import the logging library
import logging
import uuid

from django.conf import settings
from django.db import models

from bord.defaults import default_parquet_storage
from bord.fields import ParquetFileField
from bord.managers import BordManager, DelayedBordManager

# Get an instance of a logger
logger = logging.getLogger(__name__)




class BordBase(models.Model):

    parquet = ParquetFileField(verbose_name="store",storage=default_parquet_storage, upload_to="parquet", blank=True, null= True, help_text="The location of the Parquet on the Storage System (S3 or Media-URL)")
    name = models.CharField(max_length=1000, blank=True, null= True,help_text="Cleartext name")
    signature = models.CharField(max_length=300,null=True, blank=True,help_text="The Dataframes unique signature")
    unique = models.UUIDField(default=uuid.uuid4, editable=False)

    objects = BordManager()
    delayed = DelayedBordManager()

    class Meta:
        abstract = True
        
    @property
    def bord(self):
        """Accessor for the dask.Dataframe attached to the Model
        
        Raises:
            NotImplementedError: If Array does not contain a Parquet
        
        Returns:
            [dask.Dataframe] -- The dask.Dataframe
        """
        if self.parquet:
            array = self.parquet.load()
            return array
        else:
            raise NotImplementedError("This array does not have a parquet")



    def _repr_html_(self):
        return "<h1>" + f'Bord: {str(self.name)} in {self.parquet.url}' + "</h1>"




class Bord(BordBase):

    class Meta:
        abstract = True
