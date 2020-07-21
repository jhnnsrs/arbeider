import xarray as xr
from filters.logic.default import ProjectorNode

class MaxISP(ProjectorNode):
    interface = "maxisp"
    name = "Max ISP"
    path = "Max ISP"

    def project(self, array: xr.DataArray, settings: dict) -> xr.DataArray:
        return array.max(axis=3, keep_attrs=True)


class SlicedMaxISP(ProjectorNode):
    interface = "slicedmax"
    name = "Sliced Maximum Projection"
    path = "Max ISP"

    def project(self, array: xr.DataArray, settings: dict) -> xr.DataArray:
        lowerBound: int = int(settings.get("lowerBound", -1))
        upperBound: int = int(settings.get("upperBound", -1))

        array = array.sel(z=slice(lowerBound, upperBound)).max(dim="z")

        return array