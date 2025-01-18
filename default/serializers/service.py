from rest_framework import serializers
from ..models import Service
from .stage import StageSerializer


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service 
        fields = ['id', 'name']