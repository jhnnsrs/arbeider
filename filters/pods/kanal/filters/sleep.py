from kanal.backend import register_with_kanal_backend
from filters.pods.kanal.base import FilterConsumer
from filters.konfigs.filters.sleep import SleepFilter
import time
import xarray as xr


@register_with_kanal_backend(SleepFilter)
class SleepConsumer(FilterConsumer):
    """This is a Maximum Projection

    Does a Maximum Projection of the Incoming Array
    Longer class information....

    """

    def run(self,array, settings):
        return self.project(array, settings)

    def project(self, array: xr.DataArray, settings: dict) -> xr.DataArray:
        self.progress("We are sleeping 2 Seconds")
        time.sleep(2)
        self.progress("We are sleeping 14 Seconds")
        time.sleep(14)
        self.progress("We are sleeping 4 Seconds")
        time.sleep(4)
        return array.max(axis=3, keep_attrs=True)