from kanal.consumers.asynchronous.base import KanalAsyncConsumer
from kanal.consumers.sync.dask import KanalSyncConsumer
from elements.models import Representation
import xarray as xr



class FilterConsumer(KanalSyncConsumer):

    def start(self, inputs):
        rep = inputs.pop("rep")
        array = rep.array
        
        newarray = self.run(array, {})

        newrep, graph  = Representation.delayed.from_xarray(newarray, creator=self.assignation.creator, sample=rep.sample, name= self.konfig.serialize()["name"] + "of" + rep.name, chain=str(rep.chain) + "|" + self.konfig.get_interface())

        graph.compute()
        return { "rep": newrep}

    def run(self, array: xr.DataArray, settings: dict) -> xr.DataArray:
        raise NotImplementedError