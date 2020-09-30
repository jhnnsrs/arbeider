import django_filters
from django_filters import FilterSet


class ExperimentFilter(FilterSet):
    creator = django_filters.NumberFilter(field_name='creator')


class SampleFilter(FilterSet):

    creator = django_filters.NumberFilter(field_name='creator')
    experiment = django_filters.NumberFilter(field_name= "experiment__name")
    bioseries = django_filters.NumberFilter(field_name="bioseries__name",  label="The name of the desired BioSeries")