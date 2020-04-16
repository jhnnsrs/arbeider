from kanal.consumers.sync.dask import KanalSyncConsumer
from elements.models import Representation
import xarray as xr

class FilterConsumer(KanalSyncConsumer):

    def start(self, inputs):
        rep = inputs.pop("rep")
        array: xr.DataArray = rep.array

        filtered = self.run(array, inputs)

        repout, graph = Representation.delayed.from_xarray(filtered, name=f"{self.config.name} of {rep.name}", sample=rep.sample, creator=rep.creator,
                                                                           type=self.config.interface,
                                                                           chain=f'{rep.chain}|{self.config.interface}')


        self.compute(graph)
        return { "rep": repout}

    def run(self, array: xr.DataArray, settings: dict) -> xr.DataArray:
        raise NotImplementedError