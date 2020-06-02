import graphene


class BaseSerializerMutation(graphene.Mutation, abstract=True):

    @classmethod
    def __init_subclass_with_meta__(cls, **kwargs):
        super(BaseSerializerMutation, cls).__init_subclass_with_meta__(**kwargs)

    @classmethod
    def mutate(cls, *args, **kwargs):
        return cls.wrapper.mutate(*args, **kwargs)