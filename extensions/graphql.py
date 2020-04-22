from balder.register import BalderObjectWrapper, register_subscription
from balder.subscriptions import JobSubscription


@register_subscription("all_jobs", description="Get all jobs in the Right order for one Pod/Instance")
class JobWrapper(BalderObjectWrapper):
    object_type = JobSubscription


