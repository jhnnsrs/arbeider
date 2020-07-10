import graphene
from graphene.types.generic import GenericScalar

from balder.delt_types import NodeType, PodType, ProvisionType, UserType


class ProvisionFieldsMixin(object):
    id = graphene.ID(required=False, description="The Id of this Provision")
    node = graphene.Field(NodeType, required=False, description="The Node you Provisioned")
    pod = graphene.Field(PodType,required= False, description="The Provisioned Pod unique Id")
    error = graphene.String(required=False, description="The Provider of this Pod")
    status = graphene.String(required=False, description="The status of this Pod")
    reference = graphene.String(required=False, description="This Provisions reference")
    subselector = graphene.String(required=False, description="This Pods status")
    user = graphene.Field(UserType, required=False, description="This Pods status")
    provider = graphene.String(required=False, description="This Pods status")
    children = graphene.List(ProvisionType, required=False, description="This Provisions children")
    parent = graphene.Field(ProvisionType, required=False, description="This Provisions parent")


class AssignationFieldMixin(object):
    node = graphene.Field(NodeType, required=False, description="The Node you Provisioned")
    inputs = GenericScalar(blank=True, null=True, help_text="The Inputs")