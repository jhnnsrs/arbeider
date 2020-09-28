from filters.konfigs.tests import TestConfig
from kanal.registry import register_with_kanal_backend
from filters.pods.kanal.base import FilterConsumer
import xarray as xr

@register_with_kanal_backend(TestConfig)
class MaxISPConsumer(FilterConsumer):
    """This is a Maximum Projection

    Does a Maximum Projection of the Incoming Array
    Longer class information....

    """

    def run(self, array, settings):
        return self.project(array, settings)

    def project(self, array: xr.DataArray, settings: dict) -> xr.DataArray:
        return array.max(axis=3, keep_attrs=True)