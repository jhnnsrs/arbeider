from balder.register import register_query
from balder.wrappers import BalderObjectWrapper
from elements.types import SampleType
from graphene import Int
from .models import Representation, Sample
from .types import RepresentationType, SampleType


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


@register_query("representation", description="Representations by ID", id = Int(required=True))
class RepresentationWrapper(BalderObjectWrapper):
    object_type = RepresentationType
    resolver = lambda root, info, id: Representation.objects.get(id=id)
    asfield = True




@register_query("mypresentations", description="Show the latest representations for the user")
class MeQueryWrapper(BalderObjectWrapper):
    object_type = RepresentationType
    aslist = True

    @staticmethod
    def resolver(root, context):
        return Representation.objects.filter(creator=context.user).order_by("-created_at")[:5]