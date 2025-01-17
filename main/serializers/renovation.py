from rest_framework import serializers
from ..models import Renovation
from .supervisor import ProfileSerializer
from .work import WorkSerializer


class RenovationSerializer(serializers.ModelSerializer):
    progress = serializers.FloatField(read_only=True)
    supervisor = ProfileSerializer()
    work = WorkSerializer()
    
    class Meta:
        model = Renovation 
        fields = ['id', 'track', 'work', 'supervisor', 'address', 'start_date', 'end_date', 'progress']