from delt.models import Route
from django.db import models

class BalderRoute(Route):
    operation_name= models.CharField(max_length=1000, help_text="The Operation name of this endpoint")
    


