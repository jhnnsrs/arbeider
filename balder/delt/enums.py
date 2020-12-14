import graphene
from delt.enums import ClientType, Endpoint, PodStatus, AssignationStatus


PodStatusEnum = graphene.Enum.from_enum(PodStatus, description= lambda v: v)
AssignationStatusEnum = graphene.Enum.from_enum(AssignationStatus, description= lambda v: v)
ClientTypeEnum = graphene.Enum.from_enum(ClientType, description= lambda v: v)
EndpointEnum = graphene.Enum.from_enum(Endpoint, description= lambda v: v)

