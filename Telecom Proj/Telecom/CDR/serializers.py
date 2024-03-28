from rest_framework import serializers
from .models import Caller, CallDetails


class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Caller
        fields = '__all__'


class CDRSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallDetails
        fields = '__all__'
