from graphene_django import DjangoObjectType
import graphene

class BalderObjectType(DjangoObjectType):

    class Meta:
        abstract= True

class BalderMutationType(graphene.Mutation, abstract=True):

    @classmethod
    def __init_subclass_with_meta__(cls, **kwargs):
        super(BalderMutationType, cls).__init_subclass_with_meta__(**kwargs)


