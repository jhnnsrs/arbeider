import django.db.models.options as options
from django.db import models
import io
from matrise.helpers import array_to_image
from django.contrib.postgres.fields.jsonb import JSONField


from django.core.files.uploadedfile import InMemoryUploadedFile
options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('max','slicefunction',"rescale")


class ChannelsField(JSONField):
    pass



class AutoGenerateImageFromArrayMixin(models.Model):
    image = models.ImageField(null=True, blank=True)
   

    class Meta:
        abstract=True



    def save(self, *args, **kwargs):
        if not self.image:
            print("Hallo", self.image)
            array = self.store.loadDataArray()
            img = array_to_image(array, rescale=self._meta.rescale, max= self._meta.max, slicefunction = self._meta.slicefunction)
            
            img_io = io.BytesIO()
            img.save(img_io, format='jpeg', quality=100)
            image = InMemoryUploadedFile(img_io, None, self.name + ".jpeg", 'image/jpeg',
                                                img_io.tell, None)

            
            self.image = image
        super().save(*args, **kwargs)



class WithChannel(models.Model):
    channels = ChannelsField(null=True, blank=True)
   

    class Meta:
        abstract=True


    def save(self, *args, **kwargs):
        import numpy as np
        import matrise.extenders

        array = self.store.loadDataArray()
        channels = array.biometa.channels.compute().replace({np.nan:None})
        channels.columns = map(str.lower, channels.columns)
        
        self.channels = channels.to_dict(orient="records")

        super().save(*args, **kwargs)




