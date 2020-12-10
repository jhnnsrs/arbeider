from delt.models import Assignation, Node
from skille.registry import get_skille_registry

def register_skille(node: Node):
    # TODO: check if node inputs are able to handle the task (for example only allow DaskArray Type)
    
    def real_decorator(function):
            
            
            async def wrapper(graph):
                """ The function will get just the result"""
                return function(graph)




            get_skille_registry().registerGraphWorker
            return wrapper


    return real_decorator