from rest_framework import serializers
from ..models import Customer
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
import jwt
from datetime import timedelta
from django.utils.timezone import now

class SendCustomerVerificationEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, email):
        try:
            customer = Customer.objects.get(email=email)
            if customer.email_verified:
                raise serializers.ValidationError("This email is already verified.")
        except Customer.DoesNotExist:
            raise serializers.ValidationError("A customer with this email does not exist.")
        return email

class SendCustomerResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, email):
        try:
            customer = Customer.objects.get(email=email)
            if not customer:
                raise serializers.ValidationError("Customer does not exist")
        except Customer.DoesNotExist:
            raise serializers.ValidationError("A customer with this email does not exist.")
        return email
    
class CustomerResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate_password(self, password):
        if len(password) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        return password
        
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
        fields = ['id', 'firstname', 'lastname', 'email', 'email_verified']