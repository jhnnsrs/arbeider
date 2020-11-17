import graphene
from graphene.types.generic import GenericScalar


class ArrayProtocol(graphene.ObjectType):
    type = graphene.String(description="The access protocol [external, s3, network, local]")
    path = graphene.String(description="The path parameter that u can use to access")
    params = GenericScalar(description="Additional Parameters")

class CommunicationProtocol(graphene.ObjectType):
    type = graphene.String(description="The communication protocol [grapqhl, channels, kafka, ...]")
    url = graphene.String(description="The path parameter that u can use to access")

class TranscriptType(graphene.ObjectType):
    array = graphene.Field(ArrayProtocol)
    communication = graphene.Field(CommunicationProtocol)
    timestamp = graphene.DateTime()