import graphene

from delt.bouncers.context import BouncerContext


class BaseQuery(graphene.ObjectType):

  class Arguments:
        abstract = True

  @classmethod
  def Field(cls, description=None):
      arguments = dict((key, value) for key, value in vars(cls.Arguments).items() if not callable(value) and not key.startswith('__'))
      return graphene.Field(cls,  description=description or cls.__doc__, resolver=cls._resolve, **arguments)

  @classmethod
  def _resolve(cls, root, info, *args, **kwargs):
      context = BouncerContext(info=info)
      return cls.resolver(context, root, info, *args, **kwargs)

  @classmethod
  def resolver(*args,**kwargs):
      raise NotImplementedError("Please Implement the query logic")
