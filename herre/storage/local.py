from django.core.files.storage import FileSystemStorage

from herre.storage.storage import Storage


class MediaStorage(FileSystemStorage):
    pass

class ZarrStorage(FileSystemStorage):
    pass

class FilesStorage(FileSystemStorage):
    pass

class ParquetStorage(FileSystemStorage):
    pass

class LocalStorage(Storage):
    media = MediaStorage
    zarr = ZarrStorage
    files = FilesStorage
    parquet = ParquetStorage
