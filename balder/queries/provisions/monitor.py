import graphene
from graphene.types import resolver

from balder.mixins import ProvisionFieldsMixin
from balder.queries.base import BaseQuery
from balder.utils import modelToKwargs
from delt.models import Provision

class MonitorQuery(BaseQuery, ProvisionFieldsMixin):

    class Arguments:
        reference = graphene.String(required=True, description="The Pods unique reference (for the Client)")

    @classmethod
    def resolver(cls, context, root, info , reference):
        provision = Provision.objects.get(reference=reference)
        kwargs = modelToKwargs(provision)
        kwargs.pop("id")
        return cls(**kwargs)
