from balder.register import BalderObjectWrapper, register_query
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


@register_query("Representation", description="Representations by ID", id = Int(required=True))
class RepresentationWrapper(BalderObjectWrapper):
    object_type = RepresentationType
    resolver = lambda root, info, id: Representation.objects.get(id=id)
    asfield = True