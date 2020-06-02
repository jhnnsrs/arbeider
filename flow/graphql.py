from balder.register import register_mutation
from balder.wrappers import BalderMutationWrapper
from flow.balder.mutations.createflow import CreateFlowMutation
from flow.balder.mutations.toflow import ToFlowMutation


@register_mutation("createGraph", description="Create a graph from a diagram")
class CreateFlow(BalderMutationWrapper):
    mutation = CreateFlowMutation



@register_mutation("toFlow", description="Takes a Graph and creates or updates a Flow out of it")
class ToFlow(BalderMutationWrapper):
    mutation = ToFlowMutation