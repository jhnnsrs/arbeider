import graphene


class BaseMutation(graphene.Mutation, abstract=True):

    @classmethod
    def __init_subclass_with_meta__(cls, **kwargs):
        super(BaseMutation, cls).__init_subclass_with_meta__(**kwargs)