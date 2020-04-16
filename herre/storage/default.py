from django.conf import settings

from herre.storage.local import LocalStorage
from herre.storage.s3 import S3Storage
from herre.storage.storage import Storage


def get_default_storagemode() -> Storage:
    try:
        if (settings.STORAGE_MODE == "LOCAL"):
            return LocalStorage
        if (settings.STORAGE_MODE == "S3"):
            return S3Storage
        else:
            raise NotImplementedError("Storage Mode not Implemented: Try LOCAL or S3")
    except:
        raise NotImplementedError("Please specify a Storage Mode: STORAGE_MODE")
