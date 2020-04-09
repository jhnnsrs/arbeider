# import the logging library
import json
import logging
import os
import pandas as pd
import dask.dataframe as df


import xarray
from django.contrib.auth.models import User
from django.db.models.manager import Manager
from django.db.models.query import QuerySet

from elements.utils import buildRepresentationName, buildTransformationName
from larvik.generators import ArnheimGenerator
from larvik.managers import LarvikArrayManager, DelayedLarvikArrayManager
from larvik.querysets import LarvikArrayQueryset
from django.db import models

# TODO: Realiance on HDF5 Store should be nulled
from pandas import HDFStore

from django.conf import settings

# Get an instance of a logger}
logger = logging.getLogger(__name__)




class PandasManager(models.Manager):

    def create(self, **obj_data):
        if obj_data["dataframe"] is not None:
            joinedpath = os.path.join(settings.PANDAS_ROOT, obj_data["answer"] + ".h5")
            if not os.path.exists(settings.PANDAS_ROOT):
                logger.warning("Creating Directory for Pandas"+str(settings.PANDAS_ROOT))
                os.makedirs(settings.PANDAS_ROOT)

            type = obj_data["type"] if obj_data["type"] else "answers"
            vid = obj_data["vid"]
            compression = obj_data["compression"] if obj_data["compression"] else None
            with HDFStore(joinedpath) as store:
                path = type + "/" + vid
                store.put(path,obj_data["dataframe"])
                obj_data["filepath"] = joinedpath
                #TODO: Implement Compression here


            del obj_data["dataframe"]

        return super(PandasManager,self).create(**obj_data)


class RepresentationQuerySet(LarvikArrayQueryset):

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


class RepresentationGenerator(ArnheimGenerator):

    def build_name(self):
        return f"{self.model.name}"



class RepresentationManager(LarvikArrayManager):
    generatorClass = RepresentationGenerator
    group = "representation"
    use_for_related_fields = True


class DelayedRepresentationManager(DelayedLarvikArrayManager):
    generatorClass = RepresentationGenerator
    group = "representation"




class TransformationManager(LarvikArrayManager):
    use_for_related_fields = True
    group = "transformation"




class DelayedTransformationManager(DelayedLarvikArrayManager):
    group = "transformation"




class RoiQuerySet(QuerySet):

    def frame(self, *args, npartitions=1):
        values = list(self.all().values(*args))
        return df.from_pandas(pd.DataFrame.from_records(values), npartitions=npartitions)

    def _repr_html_(self):
        from django.template.loader import render_to_string
        count = self.count()
        limit = 3
        if count < limit:
            return render_to_string('ipython/rois.html', {'rois': self, "more": 0})
        else:
            return render_to_string('ipython/rois.html',
                                    {'rois': self[:limit], "more": count - limit})


class ROIManager(Manager):
    use_for_related_fields = True

    def frame(self,*args,**kwargs):
        return self.get_queryset().frame(*args,**kwargs)

    def get_queryset(self):
        return RoiQuerySet(self.model, using=self._db)


        # Python 3 syntax!!




