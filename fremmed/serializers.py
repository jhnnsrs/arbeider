from rest_framework import serializers
from fremmed.models import FrontendPod

class FrontendPodSerializer(serializers.ModelSerializer):
    class Meta:
        model = FrontendPod
        fields = "__all__"


class ActivationSerializer(serializers.Serializer):
    pod = serializers.PrimaryKeyRelatedField(queryset=FrontendPod.objects.all())
    status = serializers.CharField(max_length=1000, default="Active")
