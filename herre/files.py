import traceback
from django.core.files.storage import FileSystemStorage
import django.db.models.fields.files as files
from storages.backends.s3boto3 import S3Boto3Storage
import os
import uuid

class LocalFile(object):
    def __init__(self, field, haspath=False):
        self.field = field
        self.filename = None
        self.tmppath = "/tmp"
        self.haspath = haspath

    def __enter__(self):
        if self.haspath: return self.field.path # No TempFile Necessary
        _, file_extension = os.path.splitext(self.field.name)
        self.filename = self.tmppath + "/" + str(uuid.uuid4()) + file_extension
        with open(self.filename, 'wb+') as destination:
            for chunk in self.field.chunks():
                destination.write(chunk)

        return self.filename

    def __exit__(self, exc_type, exc_value, tb):
        if exc_type is not None:
            traceback.print_exception(exc_type, exc_value, tb)
            return False # uncomment to pass exception through
        if self.haspath:
            return True # We dont need a Temporary File of a Local File
        else:
            os.remove(self.filename)

        return True


class FieldFile(files.FieldFile):

    @property
    def local(self):
        if isinstance(self.storage, S3Boto3Storage):
            return LocalFile(self, haspath=False)
        elif isinstance(self.storage, FileSystemStorage):
            return LocalFile(self, haspath=True)
        
        raise NotImplementedError("Other Storage Formats have not been established yet. Please use S3 like Storage for time being")
