
import logging
import uuid
from json import JSONEncoder

import dask
from django.db.models.fields import BLANK_CHOICE_DASH
import xarray
import zarr as zr
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.postgres.fields.array import ArrayField
from django.contrib.postgres.fields.jsonb import JSONField
from django.db import models
from matrise.defaults import default_zarr_storage, get_default_file_version
# Create your models here.
from matrise.fields import DimsField, ShapeField, StoreField
from matrise.managers import DelayedMatriseManager, MatriseManager
from django.core.files.uploadedfile import InMemoryUploadedFile

logger = logging.getLogger(__name__)


class MatriseBase(models.Model):
    fileserializer = None


    store = StoreField(verbose_name="store",storage=default_zarr_storage, upload_to="zarr", blank=True, null= True, help_text="The location of the Array on the Storage System (S3 or Media-URL)")
    shape = ShapeField(models.IntegerField(),help_text="The arrays shape")
    dims = DimsField(models.CharField(max_length=100),help_text="The arrays dimension")
    name = models.CharField(max_length=1000, blank=True, null= True,help_text="Cleartext name")
    signature = models.CharField(max_length=300,null=True, blank=True,help_text="The arrays unique signature (check Doc on: Signatures)")
    unique = models.UUIDField(default=uuid.uuid4, editable=False, help_text="A unique identifier for this array")
    fileversion = models.CharField(max_length=1000, help_text="The File Version of this Array", default=get_default_file_version)

    objects = MatriseManager()
    delayed = DelayedMatriseManager()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    class Meta:
        abstract = True
        

    @property
    def info(self):
        return self.array.info()

    @property
    def viewer(self):
        import matrise.extenders
        return self.array.viewer

    @property
    def biometa(self):
        import matrise.extenders
        return self.array.biometa

    @property
    def array(self):
        """Accessor for the xr.DataArray class attached to the Model
        
        Raises:
            NotImplementedError: If Array does not contain a Store
        
        Returns:
            [xr.DataArray] -- The xr.DataArray class
        """
        if self.store:
            array = self.store.loadDataArray()
            return array
        else:
            raise NotImplementedError("This array does not have a store")


    @property
    def dataset(self):
        """Accessor for the xr.DataSet class attached to the Model
        
        Raises:
            NotImplementedError: If Array does not contain a Store
        
        Returns:
            [xr.Dataset] -- The Dataset 
        """
        if self.store:
            array = self.store.loadDataset()
            return array
        else:
            raise NotImplementedError("This array does not have a store")

    def _repr_html_(self):
        return "<h1>" + f'Matrise at {str(self.name)} in {self.store}' + "</h1>"



class Matrise(MatriseBase):

    class Meta:
        abstract = True
