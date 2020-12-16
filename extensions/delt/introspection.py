from elements.filters import TemplateFilter
from delt.models import Provider, Repository, Template
from balder.delt.models import ProviderType, RepositoryType, TemplateType
from graphene.types import objecttype
from balder.wrappers import BalderObjectWrapper
from balder.register import register_query
import graphene
from graphene.types.generic import GenericScalar

from balder.delt.ports import get_port_types, get_widget_types



class ListItem(graphene.ObjectType):
    key = graphene.String()
    label = graphene.String()
    description= graphene.String()
    value = GenericScalar()



@register_query("porttypes", description="Get all PortTypes in this bergen instance")
class PortTypesListWrapper(BalderObjectWrapper):
    object_type = ListItem
    resolver = lambda root, info: map(lambda item: { "key": item[0], "label": item[1].__name__, "description": item[1].__doc__}, list(get_port_types().items()))
    aslist = True

@register_query("widgettypes", description="Get all WidgetTypes in this bergen instance")
class WidgetTypesWrapper(BalderObjectWrapper):
    object_type = ListItem
    resolver = lambda root, info: map(lambda item: { "key":  item[0], "label": item[1].__name__, "description": item[1].__doc__}, list(get_widget_types().items()))
    aslist = True


@register_query("providers", description="Get all the Providers in this bergen instance")
class ProviderQueryWrapper(BalderObjectWrapper):
    object_type = ProviderType
    resolver = lambda root, info: Provider.objects.all()
    aslist = True



@register_query("templates", description="Get all the Templates in this bergen instance", withfilter=TemplateFilter)
class ProviderQueryWrapper(BalderObjectWrapper):
    object_type = TemplateType
    resolver = lambda root, info: Template.objects.all()
    aslist = True



@register_query("repositories", description="Get all the repositories for nodes in this bergen instance")
class RepositoryQueryWrapper(BalderObjectWrapper):
    object_type = RepositoryType
    resolver = lambda root, info: Repository.objects.all()
    aslist = True