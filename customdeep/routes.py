from jobb.registry import register_with_job_routes
from delt.models import Node



@register_with_job_routes
class DeepLearningJob(object):
    node = Node.objects.get(package="customdeep", interface="")


