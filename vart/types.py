import graphene
from balder.types import BalderObjectType
from vart.models import Volunteer, VartPod

class MarkType(graphene.ObjectType):
    registered = graphene.Boolean(description="Did we register your status update")


class EndType(graphene.ObjectType):
    registered = graphene.Boolean(description="Did we register the end of your assignation")


class YieldType(graphene.ObjectType):
    registered = graphene.Boolean(description="Did we register the end of your assignation")



class VartPodType(BalderObjectType):

    class Meta:
        model = VartPod



class VolunteerType(BalderObjectType):

    class Meta:
        model = Volunteer