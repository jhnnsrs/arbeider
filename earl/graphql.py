from balder.wrappers import BalderMutationWrapper
from balder.register import register_mutation
from earl.balder.mutations.serve import ServeMutation
from earl.balder.mutations.offer import OfferMutation

@register_mutation("serve", description="Serve as a Client")
class ServeMutationWrapper(BalderMutationWrapper):
    mutation = ServeMutation


@register_mutation("offer", description="Humbly offer an Implementation")
class OfferMutationWrapper(BalderMutationWrapper):
    mutation = OfferMutation