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


class DimsType(graphene.ObjectType):
    x = graphene.Int()
    y = graphene.Int()
    c = graphene.Int()
    z = graphene.Int()
    t = graphene.Int()




class PlaneType(graphene.ObjectType):
    index = graphene.Int()
    thez = graphene.Int()
    thec = graphene.Int()
    thet = graphene.Int()

    exposuretime = graphene.Float()
    deltat = graphene.Float()

    positionz = graphene.Float()
    positionx = graphene.Float()
    positiony = graphene.Float()
    positionzunit = graphene.String()


class RepresentationType(BalderObjectType):
    """ A Representation is a multi-dimensional Array that can do what ever it wants """
    channels = graphene.List(ChannelType)
    planes = graphene.List(PlaneType)

    class Meta:
        model = Representation
        description = Representation.__doc__


class SampleType(BalderObjectType):

    representations = graphene.List(RepresentationType,
                     description="The attached Representations",
                     name = graphene.String(description="Filtered by Name", required=False),
                     dims = graphene.List(graphene.String, description="The dimensions required", required=False)
                     
                     
                     )

    def resolve_representations(parent, info, *args, **kwargs):

        queryset = parent.representations
        if "dims" in kwargs: queryset = queryset.filter(dims__contains=kwargs["dims"])
        if "name" in kwargs: queryset = queryset.filter(name=kwargs["name"])
        return queryset.all()

    class Meta:
        model = Sample
        description = Sample.__doc__


class ROIType(BalderObjectType):
    class Meta:
        model = ROI
        description = ROI.__doc__