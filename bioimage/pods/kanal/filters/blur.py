from kanal.registry import register_with_kanal_backend
from filters.pods.kanal.base import FilterConsumer
from filters.configs.filters.blur import BlurFilterKonfig
import xarray as xr


@register_with_kanal_backend(BlurFilterKonfig)
class BlurConsumer(FilterConsumer):
    """This is a Maximum Projection

    Does a Maximum Projection of the Incoming Array
    Longer class information....

    """

    def run(self,array, settings):
        raise NotImplementedError("Node Does not Exist")
        return self.project(array, settings)

    def project(self, array: xr.DataArray, settings: dict) -> xr.DataArray:
        return array.max(axis=3, keep_attrs=True)