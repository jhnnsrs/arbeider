import django_filters
from delt.models import Node

class NodeListFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    
    class Meta:
         model = Node
         fields = ["name"]