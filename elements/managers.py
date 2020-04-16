# import the logging library
import json
import logging
import os

import dask.dataframe as df
import pandas as pd
import xarray
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.manager import Manager
from django.db.models.query import QuerySet
# TODO: Realiance on HDF5 Store should be nulled
from pandas import HDFStore

from bord.managers import BordManager
from elements.utils import buildRepresentationName, buildTransformationName
from herre.generators import ArnheimNameGenerator
from matrise.managers import DelayedMatriseManager, MatriseManager
from matrise.querysets import MatriseQueryset

# Get an instance of a logger}
logger = logging.getLogger(__name__)



class RepresentationQuerySet(MatriseQueryset):

    def delete(self):
        for rep in self.all():
            rep.delete

    def _repr_html_(self):
        from django.template.loader import render_to_string
        count = self.count()
        limit = 3
        if count < limit:
            return render_to_string('ipython/representation.html', {'representations': self, "more": 0})
        else:
            return render_to_string('ipython/representation.html', {'representations': self[:limit], "more": count - limit})


class RepresentationGenerator(ArnheimNameGenerator):

    def build_name(self):
        return f"{self.instance.name}"



class RepresentationManager(MatriseManager):
    generatorClass = RepresentationGenerator
    group = "representation"
    use_for_related_fields = True


class DelayedRepresentationManager(DelayedMatriseManager):
    generatorClass = RepresentationGenerator
    group = "representation"




class TransformationManager(MatriseManager):
    use_for_related_fields = True
    group = "transformation"


class TableManager(BordManager):
    group = "table"

class DelayedTransformationManager(DelayedMatriseManager):
    group = "transformation"



class ROIManager(Manager):
    use_for_related_fields = True

    def frame(self,*args,**kwargs):
        return self.get_queryset().frame(*args,**kwargs)



        # Python 3 syntax!!
