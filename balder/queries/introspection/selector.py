from balder.delt.models import ProvisionType, SelectorType
import graphene
from graphene.types import resolver

from balder.queries.base import BaseQuery
from balder.utils import modelToDict
from delt.models import Provision, Selector

class SelectorQuery(BaseQuery):
    Output = SelectorType

    class Arguments:
        provider = graphene.String(required=True, description="The Provider you want to find for")

    @classmethod
    def resolver(cls, context, root, info , *args, **kwargs):
        selector = Selector.objects.get(provider__name=kwargs["provider"])
        return selector