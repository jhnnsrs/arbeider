from elements.mutations.create_sample import CreateSampleMutation
from elements.filters import RepresentationFilter, SampleFilter
from elements.mutations.update_representation import UpdateRepresentationMutation
from elements.mutations.create_representation import CreateRepresentationMutation
from balder.register import register_mutation, register_query
from balder.wrappers import BalderMutationWrapper, BalderObjectWrapper
from elements.types import SampleType
import graphene 
from .models import Representation, Sample
from .types import ChannelType, DimsType, RepresentationType, SampleType


@register_query("representations", description="All Representations", withfilter=RepresentationFilter)
class AllRepresentationWrapper(BalderObjectWrapper):
    object_type = RepresentationType
    resolver = lambda root, info: Representation.objects.all()
    aslist = True


@register_query("samples", description="All Samples", withfilter=SampleFilter)
class SampleWrapper(BalderObjectWrapper):
    object_type = SampleType
    resolver = lambda root, info: Sample.objects.all()
    aslist = True


@register_query("sample", description="Sample by ID", id = graphene.ID(description="The id of the sample"))
class SampleWrapper(BalderObjectWrapper):
    object_type = SampleType
    resolve = lambda context, id : Sample.objects.get(id=id)
    asfield = True


@register_query("representation", description="Representations by ID", id = graphene.Int(required=True))
class RepresentationWrapper(BalderObjectWrapper):
    object_type = RepresentationType
    resolve = lambda context, id: Representation.objects.get(id=id)
    asfield = True


@register_mutation("createRepresentation", description="Create Representation")
class CreateRepresentationWrapper(BalderMutationWrapper):
    mutation = CreateRepresentationMutation


@register_mutation("createSample", description="Create Sample")
class CreateRepresentationWrapper(BalderMutationWrapper):
    mutation = CreateSampleMutation



@register_mutation("updateRepresentation", description="Update Representation")
class CreateRepresentationWrapper(BalderMutationWrapper):
    mutation = UpdateRepresentationMutation



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



@register_query("myrepresentations", description="Show the latest representations for the user")
class MeQueryWrapper(BalderObjectWrapper):
    object_type = RepresentationType
    aslist = True
    resolve= lambda context: Representation.objects.filter(sample__creator=context.user).order_by("-created_at")[:5]