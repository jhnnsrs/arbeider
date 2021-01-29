from balder.delt.models import DataModelType, DataPointsType, UserType
import graphene
from graphene.types.generic import GenericScalar


class ArrayProtocol(graphene.ObjectType):
    type = graphene.String(description="The access protocol [external, s3, network, local]")
    path = graphene.String(description="The path parameter that u can use to access")
    params = GenericScalar(description="Additional Parameters")

class CommunicationProtocol(graphene.ObjectType):
    type = graphene.String(description="The communication protocol [grapqhl, channels, kafka, ...]")
    url = graphene.String(description="The path parameter that u can use to access")

class PostmanProtocol(graphene.ObjectType):
    type = graphene.String(description="The communication protocol [grapqhl, channels, kafka, ...]")
    kwargs = GenericScalar(description="kwargs for your postman")

class TranscriptType(graphene.ObjectType):
    array = graphene.Field(ArrayProtocol)
    communication = graphene.Field(CommunicationProtocol)
    postman = graphene.Field(PostmanProtocol)
    extensions = GenericScalar(description="Configuration space for extensios")
    timestamp = graphene.DateTime()
    models = graphene.List(DataModelType, description="Extensionsmap of Identifier and Model")
    points = graphene.List(DataPointsType, description="The Attached datapoints to this instance")
    user = graphene.Field(UserType)
