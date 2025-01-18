from rest_framework import serializers
from ..models import Work
from .stage import StageSerializer


class WorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Work 
        fields = ['id', 'name']