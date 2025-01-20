from rest_framework import serializers
from ..models import Service

class ServiceSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = Service 
        fields = ['id', 'name']

    def get_name(self, obj):
        return obj.service_type.name if obj.service_type else None
    