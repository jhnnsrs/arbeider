from skille.decorators import register_skille
from delt.models import Node



@register_skille(Node.objects.get(id=7), mappable=True, bag=True)
def massive_mapping(graph):
    return graph

