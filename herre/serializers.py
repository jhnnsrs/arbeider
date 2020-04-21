from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Profile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=get_user_model()
        fields=["id","username","first_name","last_name"]

class ProfileSerializer(serializers.ModelSerializer):
    user= UserSerializer()

    class Meta:
        model=Profile
        fields='__all__'
