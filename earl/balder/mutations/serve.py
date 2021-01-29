from earl.balder.types import PeasentType
from balder.scalars.models import NodeID
import logging
import uuid

import graphene
from graphene.types.generic import GenericScalar

from balder.delt.models import AssignationType
from balder.mutations.base import BaseMutation
from earl.models import Peasent
logger = logging.getLogger(__name__)


class NoPodFoundError(Exception):
    pass

class ServeMutation(BaseMutation):
    Output = PeasentType

    class Arguments:
        name = graphene.String(required=True, description="The unique name you shall henve be known for")

    @classmethod
    def change(cls, context, root, info, *arg, name = None):
        
        peasent, created = Peasent.objects.get_or_create(name=name, defaults = {
            "application": context.auth.application
        })

        return peasent
        
