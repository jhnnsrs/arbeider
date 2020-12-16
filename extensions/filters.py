import django_filters
from delt.models import Node

class NodeListFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    repository = django_filters.NumberFilter(field_name="repository", lookup_expr="exact")
    
    class Meta:
         model = Node
         fields = ["name","repository"]