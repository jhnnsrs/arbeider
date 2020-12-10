import graphene
from delt.enums import PodStatus, AssignationStatus


PodStatusEnum = graphene.Enum.from_enum(PodStatus, description= lambda v: v)
AssignationStatusEnum = graphene.Enum.from_enum(AssignationStatus, description= lambda v: v)

