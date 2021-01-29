from delt.models import Node, Provider
from earl.balder.types import PeasentTemplateType, PeasentType
from balder.scalars.models import NodeID
import logging
import uuid

import graphene
from graphene.types.generic import GenericScalar

from balder.delt.models import AssignationType
from balder.mutations.base import BaseMutation
from earl.models import Peasent, PeasentTemplate
logger = logging.getLogger(__name__)
from delt.template.integrity import template_identifier


peasent_provider, created = Provider.objects.get_or_create(name="peasent")



class NoPodFoundError(Exception):
    pass

class OfferMutation(BaseMutation):
    Output = PeasentTemplateType

    class Arguments:
        node = graphene.ID(required=True, description="The Node you offer to give an implementation for")
        peasent = graphene.ID(required=True, description="The Peasent you are offering for") #TODO: Fact check that you wouldn't be offering for another application assert Peasent.Application
        params  = GenericScalar(required=False, description="Some additional Params for your offering")

    @classmethod
    def change(cls, context, root, info, *arg, **kwargs):

        node = Node.objects.get(id=kwargs.get("node"))
        peasent = Peasent.objects.get(id=kwargs.get("peasent"))
        params = kwargs.get("params", {})

        hash = template_identifier(node, params)

        try:
            return PeasentTemplate.objects.get(identifier=hash)
        except:
            peasent_template = PeasentTemplate.objects.create(
                node=node,
                params=params,
                provider=peasent_provider,
                peasent=peasent,
                identifier=hash
            )
            return peasent_template
        
