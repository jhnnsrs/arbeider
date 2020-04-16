from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage

from herre.storage.storage import Storage


class MediaStorage(S3Boto3Storage):
    bucket_name = settings.MEDIA_BUCKET
    custom_domain = f"{settings.S3_PUBLIC_DOMAIN}/{bucket_name}"


class ZarrStorage(S3Boto3Storage):
    bucket_name = settings.ZARR_BUCKET
    custom_domain = f"{settings.S3_PUBLIC_DOMAIN}/{bucket_name}"


class FilesStorage(S3Boto3Storage):
    bucket_name = settings.FILES_BUCKET
    custom_domain = f"{settings.S3_PUBLIC_DOMAIN}/{bucket_name}"

class ParquetStorage(S3Boto3Storage):
    bucket_name = settings.PARQUET_BUCKET
    custom_domain = f"{settings.S3_PUBLIC_DOMAIN}/{bucket_name}"


class S3Storage(Storage):
    media = MediaStorage
    zarr = ZarrStorage
    files = FilesStorage
    parquet = ParquetStorage
