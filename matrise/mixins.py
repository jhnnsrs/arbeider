import django.db.models.options as options
from django.db import models
import io
from matrise.helpers import array_to_image

from django.core.files.uploadedfile import InMemoryUploadedFile
options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('max','slicefunction',"rescale")


class AutoGenerateImageFromArrayMixin(models.Model):
    image = models.ImageField(null=True, blank=True)
   

    class Meta:
        abstract=True



    def save(self, *args, **kwargs):
        print("Hallo", self.image)
        array = self.store.loadDataArray()
        img = array_to_image(array, rescale=self._meta.rescale, max= self._meta.max, slicefunction = self._meta.slicefunction)
        
        img_io = io.BytesIO()
        img.save(img_io, format='jpeg', quality=100)
        image = InMemoryUploadedFile(img_io, None, self.name + ".jpeg", 'image/jpeg',
                                            img_io.tell, None)

        
        self.image = image
        super().save(*args, **kwargs)



