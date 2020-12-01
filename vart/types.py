import graphene
from balder.types import BalderObjectType
from vart.models import Volunteer

class MarkType(graphene.ObjectType):
    registered = graphene.Boolean(description="Did we register your status update")


class VolunteerType(BalderObjectType):

    class Meta:
        model = Volunteer