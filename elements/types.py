from graphene_django import DjangoObjectType
from elements.models import Representation, Sample


class RepresentationType(DjangoObjectType):
    """ A Representation is a multi-dimensional Array that can do what ever it wants """
    class Meta:
        model = Representation
        description = Representation.__doc__


class SampleType(DjangoObjectType):
    class Meta:
        model = Sample
        description = Sample.__doc__