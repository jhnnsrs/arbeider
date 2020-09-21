from kanal.consumers.sync.dask import KanalSyncConsumer
from elements.models import Representation
import xarray as xr

class FilterConsumer(KanalSyncConsumer):

    def start(self, inputs):
        rep = inputs.pop("rep")
        array: xr.DataArray = rep.array

        filtered = self.run(array, inputs)

        repout, graph = Representation.delayed.from_xarray(filtered, name=f"{self.konfig.name} of {rep.name}", sample=rep.sample, creator=self.assignation.creator,
                                                                           type=self.konfig.interface,
                                                                           chain=f'{rep.chain}|{self.konfig.interface}')


        graph.compute()
        return { "rep": repout}

    def run(self, array: xr.DataArray, settings: dict) -> xr.DataArray:
        raise NotImplementedError