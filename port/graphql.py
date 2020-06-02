from balder.register import register_mutation
from balder.wrappers import BalderMutationWrapper
from flow.balder.mutations import CreateFlowMutation


@register_mutation("createFlow", description="Create a flow from a Diagram")
class CreateFlow(BalderMutationWrapper):
    mutation = CreateFlowMutation