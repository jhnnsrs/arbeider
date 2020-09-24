from rest_framework import serializers
from konfig.params import Model
from elements.models import Antibody, Experiment, Sample, ExperimentalGroup, Animal, FileMatchString, Representation, \
    ROI, Transformation


class AntibodySerializer(Model):
    class Meta:
        model = Antibody
        fields = "__all__"

class AnimalSerializer(Model):

    class Meta:
        model = Animal
        fields = "__all__"

class FileMatchStringSerializer(Model):
    class Meta:
        model = FileMatchString
        fields = "__all__"

class ExperimentSerializer(Model):
    class Meta:
        model = Experiment
        fields = "__all__"

class ExperimentalGroupSerializer(Model):
    class Meta:
        model = ExperimentalGroup
        fields = "__all__"

class RepresentationSerializer(Model):
    class Meta:
        model = Representation
        fields = "__all__"

class TransformationSerializer(Model):
    class Meta:
        model = Transformation
        fields = "__all__"


class ROISerializer(Model):
    class Meta:
        model = ROI
        fields = "__all__"



class SampleSerializer(Model):
    representations = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    bioseries = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Sample
        fields = "__all__"


