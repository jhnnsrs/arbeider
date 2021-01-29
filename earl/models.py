from django.db import models
from delt.models import ArnheimApplication, Pod, Template
import namegenerator
# Create your models here.

class Peasent(models.Model):
    name = models.CharField(max_length=300, default=namegenerator.gen, unique=True)
    application = models.ForeignKey(ArnheimApplication, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"

class PeasentTemplate(Template):
    peasent = models.ForeignKey(Peasent, on_delete=models.CASCADE)


    def __str__(self):
        return super().__str__() + f" at {self.peasent.name}"




class PeasentPod(Pod):
    channel = models.CharField(max_length=5000, help_text="The channel where the Pod listens to", default="none")
    pass

