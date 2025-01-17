from rest_framework import serializers
from ..models import Work
from .stage import StageSerializer

class WorkSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = Work 
        fields = ['id', 'name']

    def get_name(self, obj):
        return obj.work_type.name if obj.work_type else None
    