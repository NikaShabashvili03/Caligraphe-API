from rest_framework import serializers
from ..models import Supervisor
    
class SupervisorLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        try:
            supervisor = Supervisor.objects.get(email=data['email'])
            if supervisor.check_password(data['password']):
                return supervisor
            else:
                raise serializers.ValidationError("Invalid credentials")
        except Supervisor.DoesNotExist:
            raise serializers.ValidationError("Supervisor does not exist")
        
class SupervisorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supervisor 
        fields = ['id', 'firstname', 'lastname', 'email']