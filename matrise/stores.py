
import asyncio
import s3fs
import xarray as xr
import zarr
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db.models.fields.files import FieldFile
from storages.backends.s3boto3 import S3Boto3Storage
from zarr import blosc
import logging

logger = logging.getLogger(__name__)



compressor = blosc.Blosc(cname='zstd', clevel=3, shuffle=blosc.Blosc.BITSHUFFLE)
blosc.use_threads = True

zarr.storage.default_compressor = compressor

class NotCompatibleException(Exception):
    pass



class XArrayStore(FieldFile):

    def _getStore(self):
        if isinstance(self.storage, S3Boto3Storage):
            bucket = self.storage.bucket_name
            location = self.storage.location
            s3_path = f"{bucket}/{self.name}"
            # Initilize the S3 file system
            logger.info(f"Bucket [{bucket}]: Connecting to {self.name}")
            s3 = s3fs.S3FileSystem(client_kwargs={"endpoint_url": settings.AWS_S3_ENDPOINT_URL})
            store = s3fs.S3Map(root=s3_path, s3=s3)
            return store
        if isinstance(self.storage, FileSystemStorage):
            location = self.storage.location
            path = f"{location}/{self.name}"
            # Initilize the S3 file system
            logger.info(f"Folder [{location}]: Connecting to {self.name}")
            store = zarr.DirectoryStore(path)
            return store
        else:
            raise NotImplementedError("Other Storage Formats have not been established yet. Please use S3 like Storage for time being")

    @property
    def connected(self):
        return self._getStore()

    def save(self, array, compute=True, apiversion = settings.MATRISE_APIVERSION, fileversion= settings.MATRISE_FILEVERSION):
        if self.instance.unique is None: raise Exception("Please assign a Unique ID first")
        dataset = None
        if apiversion == "0.1":
            dataset = array.to_dataset(name="data")
            dataset.attrs["apiversion"] = apiversion
            dataset.attrs["fileversion"] = fileversion
            if fileversion == "0.1":
                dataset.attrs["model"] = str(self.instance.__class__.__name__)
                dataset.attrs["unique"] = str(self.instance.unique)
            else:
                raise NotImplementedError("This FileVersion has not been Implemented yet")

        else:
            raise NotImplementedError("This API Version has not been Implemented Yet")

        try:
            logger.info(f"Saving File with API v.{apiversion}  and File v.{fileversion} ")
            print(self.connected)
            return dataset.to_zarr(store=self.connected, mode="w", compute=compute, consolidated=True)
        except Exception as e:
            raise e

    def loadDataArray(self, apiversion = settings.MATRISE_APIVERSION):
        dataset = xr.open_zarr(store=self.connected, consolidated=False)
        fileversion = dataset.attrs["fileversion"]
        fileapiversion = dataset.attrs["apiversion"]
        if apiversion == "0.1":
            if  fileapiversion == "0.1" and  fileversion == "0.1":
                logger.info(f"Opening File with API v.{apiversion}  and File v.{fileversion} ")
                import matrise.extenders as e
                array = dataset["data"]
                array.name = self.instance.name
                return array
            else:
                raise NotCompatibleException(f"The ApiVersion v.{apiversion} is not able to parse file with API v.{fileapiversion} and File v.{fileversion}")
        else: NotImplementedError("This API Version has not been Implemented Yet")


    def loadDataset(self):
        return xr.open_zarr(store=self.connected, consolidated=False)

