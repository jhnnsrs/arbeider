from balder.delt.models import ProvisionType
import graphene
from graphene.types import resolver

from balder.queries.base import BaseQuery
from balder.utils import modelToDict
from delt.models import Provision

class MonitorQuery(BaseQuery):
    Output = ProvisionType

    class Arguments:
        reference = graphene.String(required=True, description="The Pods unique reference (for the Client)")

    @classmethod
    def resolver(cls, context, root, info , reference):
        provision = Provision.objects.get(reference=reference)
        kwargs = modelToDict(provision)
        return ProvisionType(**kwargs)
