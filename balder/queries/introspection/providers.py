from balder.delt.models import ProviderType, ProvisionType, SelectorType, TemplateType
from balder.delt.models import ProvisionType, SelectorType
import graphene
from graphene.types import resolver

from balder.queries.base import BaseQuery
from balder.utils import modelToDict
from delt.models import Provision, Selector, Template


class TemplateQuery(BaseQuery):
    Output = graphene.List(TemplateType)

    class Arguments:
        provider = graphene.String(required=False, description="The Provider you want to find for")

    @classmethod
    def resolver(cls, context, root, info , *args, **kwargs):
        provider = kwargs.get("provider", None)



        templates = Template.objects.filter(provider__name=provider)
        return templates