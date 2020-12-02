
from vart.subscriptions.host import HostSubscription
from vart.subscriptions.queue import QueueSubscription
from vart.mutations.volunteer import VolunteerMutation
from vart.mutations.mark import MarkMutation
from balder.wrappers import (BalderMutationWrapper, BalderObjectWrapper, BalderSubscriptionWrapper)
from balder.register import (register_mutation, register_query,
                             register_subscription)



@register_mutation("mark", description="Mark your pods status")
class Mark(BalderMutationWrapper):
    mutation = MarkMutation


@register_mutation("volunteer", description="Volunteer for hosting a Node")
class Volunteer(BalderMutationWrapper):
    mutation = VolunteerMutation



@register_subscription("queue", description="The waiting list for volunteering")
class Queue(BalderSubscriptionWrapper):
    subscription = QueueSubscription



@register_subscription("host", description="The interface for hosting a pod")
class Host(BalderSubscriptionWrapper):
    subscription = HostSubscription