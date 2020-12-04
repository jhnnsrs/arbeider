from elements.mutations.create_representation import CreateRepresentationMutation
from balder.register import register_mutation, register_query
from balder.wrappers import BalderMutationWrapper, BalderObjectWrapper
from elements.types import SampleType
import graphene 
from .models import Representation, Sample
from .types import ChannelType, DimsType, RepresentationType, SampleType


@register_query("allRepresentation", description="All Representations")
class AllRepresentationWrapper(BalderObjectWrapper):
    object_type = RepresentationType
    resolver = lambda root, info: Representation.objects.all()
    aslist = True


@register_query("allSamples", description="All Representations")
class SampleWrapper(BalderObjectWrapper):
    object_type = SampleType
    resolver = lambda root, info: Sample.objects.all()
    aslist = True


@register_query("representation", description="Representations by ID", id = graphene.Int(required=True))
class RepresentationWrapper(BalderObjectWrapper):
    object_type = RepresentationType
    resolver = lambda root, info, id: Representation.objects.get(id=id)
    asfield = True


@register_mutation("createRepresentation", description="Representations by ID", id = graphene.Int(required=True))
class CreateRepresentationWrapper(BalderMutationWrapper):
    mutation = CreateRepresentationMutation




@register_query("channelsof", description="Channel of a Representation", rep = graphene.Int(required=True, ))
class ChannelsOfWrapper(BalderObjectWrapper):
    object_type = ChannelType
    resolver = lambda root, info, rep: Representation.objects.get(id=rep).channels
    aslist = True

@register_query("dimsof", description="Channel of a Representation", rep = graphene.Int(required=True, ))
class ChannelsOfWrapper(BalderObjectWrapper):
    object_type = DimsType
    resolver = lambda root, info, rep: dict(zip(Representation.objects.get(id=rep).dims,Representation.objects.get(id=rep).shape))
    asfield = True



@register_query("mypresentations", description="Show the latest representations for the user")
class MeQueryWrapper(BalderObjectWrapper):
    object_type = RepresentationType
    aslist = True
    resolve= lambda context: Representation.objects.filter(creator=context.user).order_by("-created_at")[:5]