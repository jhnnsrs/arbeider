import graphene
from graphene_django import DjangoObjectType

from balder.registry import register_with_schema
from delt.models import Job, Node


class JobType(DjangoObjectType):
    class Meta:
        model = Job


class JobQuery(object):
    all_jobs = graphene.List(JobType)
    test = graphene.List(graphene.String)

    def __init__(self,*args, **kwargs):
        print(args, kwargs)
        super().__init__(*args, **kwargs)

    def resolve_all_jobs(self, info, **kwargs):
        return Job.objects.all()

    def resolve_test(self, info, **kwargs):
        return ["hallo"]


class NodeType(DjangoObjectType):
    class Meta:
        model = Node


@register_with_schema
class Dynamic(object):
    pass
    