


from balder.scalars.foreignkey import ForeignKey
from delt.models import Node

class NodeID(ForeignKey):
    queryset = Node.objects