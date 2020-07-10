from builtins import classmethod

import graphene

from delt.bouncers.context import BouncerContext


class BaseMutation(graphene.Mutation, abstract=True):

    @classmethod
    def __init_subclass_with_meta__(cls, **kwargs):
        super(BaseMutation, cls).__init_subclass_with_meta__(**kwargs)


    @classmethod
    def change(cls, context: BouncerContext, root, info, *args,  **kwargs):
        raise NotImplementedError("Please overwrite this")


    @classmethod
    def mutate(cls, root, info, *args, **kwargs):
        context = BouncerContext(info=info)
        return cls.change(context, root, info, *args, **kwargs)