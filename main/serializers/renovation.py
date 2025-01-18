from rest_framework import serializers
from ..models import Renovation
from .supervisor import ProfileSerializer
from .service import ServiceSerializer


class RenovationSerializer(serializers.ModelSerializer):
    progress = serializers.FloatField(read_only=True)
    supervisor = ProfileSerializer()
    service = ServiceSerializer()
    
    class Meta:
        model = Renovation 
        fields = ['id', 'track', 'service', 'supervisor', 'address', 'start_date', 'end_date', 'progress']