import xarray as xr

from delt.node import BackendNodeType
from filters.models import Filter

class FilterNode(BackendNodeType):
    package = "@canonical/filters/filter"   
    variety = "filter"
    register = Filter

    def filter(self, array: xr.DataArray, settings: dict) -> xr.DataArray:
        raise NotImplementedError



class ProjectorNode(BackendNodeType):
    package = "@canonical/filters/projections"
    variety = "projection"
    register = Filter

    def project(self, array: xr.DataArray, settings: dict) -> xr.DataArray:
        raise NotImplementedError