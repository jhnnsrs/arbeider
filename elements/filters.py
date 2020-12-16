import django_filters
from django_filters import FilterSet
from delt.models import Template


class ExperimentFilter(FilterSet):
    creator = django_filters.NumberFilter(field_name='creator')


class SampleFilter(FilterSet):

    creator = django_filters.NumberFilter(field_name='creator')
    experiment = django_filters.NumberFilter(field_name= "experiment__name")
    bioseries = django_filters.NumberFilter(field_name="bioseries__name",  label="The name of the desired BioSeries")


class TemplateFilter(django_filters.FilterSet):
    provider = django_filters.CharFilter(field_name="provider__name", label="The name of the provider")
    node = django_filters.NumberFilter(field_name="node", label="The node you want to filter for")
    
    class Meta:
         model = Template
         fields = ["provider","node"]