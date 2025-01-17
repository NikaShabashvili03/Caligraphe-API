from rest_framework import serializers
from ..models import Work
from .stage import StageSerializer


class WorkSerializer(serializers.ModelSerializer):
    stages = StageSerializer(many=True, read_only=True)

    class Meta:
        model = Work 
        fields = ['id', 'name', 'stages']