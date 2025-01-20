from rest_framework import serializers
from ..models import Customer

class CustomerRegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    firstname = serializers.CharField(write_only=True)
    lastname = serializers.CharField(write_only=True)

    def validate_email(self, email):
        if Customer.objects.filter(email=email).exists():
            raise serializers.ValidationError("A customer with this email already exists.")
        return email

    def create(self, validated_data):
        customer = Customer.objects.create(
            email=validated_data['email'],
            password=validated_data['password'],
            firstname=validated_data['firstname'],
            lastname=validated_data['lastname'],
        )
        return customer
        
class CustomerLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        try:
            customer = Customer.objects.get(email=data['email'])
            if customer.check_password(data['password']):
                return customer
            else:
                raise serializers.ValidationError("Invalid credentials")
        except Customer.DoesNotExist:
            raise serializers.ValidationError("Customer does not exist")
        
class CustomerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer 
        fields = ['id', 'firstname', 'lastname', 'email']