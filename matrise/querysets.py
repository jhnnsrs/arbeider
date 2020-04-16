import xarray
from dask.bag import Bag
from django.db.models.query import QuerySet
import dask.bag as db
import dask.dataframe as dd
from dask.bag.core import Bag



class MatriseQueryset(QuerySet):
    pass