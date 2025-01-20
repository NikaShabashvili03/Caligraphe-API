from rest_framework import serializers
from ..models import Renovation
from authentication.serializers.supervisor import SupervisorProfileSerializer
from authentication.serializers.customer import CustomerProfileSerializer
from .service import ServiceSerializer

class RenovationSerializer(serializers.ModelSerializer):
    progress = serializers.FloatField(read_only=True)
    supervisor = SupervisorProfileSerializer()
    customer = CustomerProfileSerializer()
    service = ServiceSerializer()
    
    class Meta:
        model = Renovation 
        fields = ['id', 'track', 'service', 'supervisor', 'customer', 'address', 'start_date', 'end_date', 'progress']