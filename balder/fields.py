from functools import partial
from os import stat
from graphene.types.generic import GenericScalar
from graphene.types import String
from graphene import Field, List
from graphene_django.filter.utils import (get_filtering_args_from_filterset,
                                          get_filterset_class)
from pandas.core.tools.datetimes import Scalar




class Inputs(GenericScalar):
    """This is the Nodes Input Representation"""


class Outputs(GenericScalar):
    """ This is the Nodes Outputs """


class ImageField(Field):
    ''' This is the Image field '''
    def __init__(self, imagefield, *args, **kwargs) -> None:
        self.imagefield = imagefield
        super().__init__(String, *args, **kwargs)

    @staticmethod
    def url_resolver(field, root, info, *args, **kwargs):
        instance = getattr(root, field.attname)
        return instance.url if instance else None

    def get_resolver(self, parent_resolver):
        return partial(self.url_resolver, self.imagefield)



class BalderFilterField(Field):
    '''
    Custom field to use django-filter with graphene object types (without relay).
    '''

    def __init__(self, _type, fields=None, extra_filter_meta=None,
                 filterset_class=None, *args, **kwargs):
        _fields = _type._meta.filter_fields
        _model = _type._meta.model
        self.of_type = _type
        self.fields = fields or _fields
        meta = dict(model=_model, fields=self.fields)
        if extra_filter_meta:
            meta.update(extra_filter_meta)
        self.filterset_class = get_filterset_class(filterset_class, **meta)
        self.filtering_args = get_filtering_args_from_filterset(
            self.filterset_class, _type)
        kwargs.setdefault('args', {})
        kwargs['args'].update(self.filtering_args)
        super().__init__(List(_type), *args, **kwargs)

    @staticmethod
    def list_resolver(manager, filterset_class, filtering_args, root, info, *args, **kwargs):
        #TODO: here it would be good to filter for permissions if it is ndeeded
        
        filter_kwargs = {k: v for k,
                         v in kwargs.items() if k in filtering_args}
        qs = manager.get_queryset()
        qs = filterset_class(data=filter_kwargs, queryset=qs).qs
        return qs

    def get_resolver(self, parent_resolver):
        return partial(self.list_resolver, self.of_type._meta.model._default_manager,
                       self.filterset_class, self.filtering_args)



class BalderField(Field):
    pass
