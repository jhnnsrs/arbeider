from balder.types import BalderObjectType
from elements.models import ROI, Representation, Sample
import graphene

class ChannelType(graphene.ObjectType):
    name = graphene.String()
    color = graphene.String()
    index = graphene.Int()
    aquisitionmode = graphene.String()
    samplesperpixel = graphene.Int()
    emissionwavelength = graphene.Float()
    excitationwavelength = graphene.Float()



class RepresentationType(BalderObjectType):
    """ A Representation is a multi-dimensional Array that can do what ever it wants """
    channels = graphene.List(ChannelType)

    class Meta:
        model = Representation
        description = Representation.__doc__


class SampleType(BalderObjectType):
    class Meta:
        model = Sample
        description = Sample.__doc__


class ROIType(BalderObjectType):
    class Meta:
        model = ROI
        description = ROI.__doc__