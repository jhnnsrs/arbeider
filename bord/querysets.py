import xarray
from dask.bag import Bag
from django.db.models.query import QuerySet
import dask.bag as db
import dask.dataframe as dd
from dask.bag.core import Bag

class BordQueryset(QuerySet):

    def delete(self):
        for el in self.all():
            el.zarr.delete()


    def combine(self):
        """Should Combine the queryset to one DataTable
        
        Returns:
            [type] -- [description]
        """
        raise NotImplementedError
