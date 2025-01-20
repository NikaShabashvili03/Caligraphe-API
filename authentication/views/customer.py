from rest_framework import generics, status
from rest_framework.response import Response
from authentication.serializers.customer import CustomerLoginSerializer, CustomerProfileSerializer, CustomerRegisterSerializer
from ..models.session import Session
from django.middleware.csrf import get_token
import uuid
from rest_framework import status
from datetime import timedelta
from rest_framework.permissions import AllowAny, IsAuthenticated
from authentication.permissions import IsCustomer
from django.utils.timezone import now
from django.utils.timezone import make_aware


class CustomerRegisterView(generics.GenericAPIView):
    serializer_class = CustomerRegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        new_customer = serializer.save()

        token = str(uuid.uuid4())
        expires_at = now() + timedelta(days=2)

        session = Session.objects.create(
            customer=new_customer,
            session_token=token,
            expires_at=expires_at,
        )

        customer_data = CustomerProfileSerializer(new_customer).data

        response = Response(customer_data, status=status.HTTP_201_CREATED)
        response.set_cookie(
            'sessionId', session.session_token, expires=expires_at
        )
        csrf_token = get_token(request)
        response['X-CSRFToken'] = csrf_token

        return response

class CustomerLoginView(generics.GenericAPIView):
    serializer_class = CustomerLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        csrf_token = get_token(request)
        
        customer = serializer.validated_data

        token = str(uuid.uuid4())
        customer.last_login = now()
        customer.save()

        expires_at = now() + timedelta(days=2)

        session = Session.objects.create(
            customer=customer,
            session_token=token,
            expires_at=expires_at,
        )
        
        customer_data = CustomerProfileSerializer(customer).data
        
        response = Response(customer_data, status=status.HTTP_200_OK)
        response.set_cookie(
            'sessionId',
            session.session_token,
            expires=expires_at, 
        )
        response['X-CSRFToken'] = csrf_token
        return response

class CustomerLogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, IsCustomer]

    def post(self, request, *args, **kwargs):
        customer = request.user.customer
        sessions = Session.objects.filter(customer_id=customer)
        response = Response({'details': 'Logged out successfully'}, status=status.HTTP_200_OK)
        if sessions:
            sessions.delete()
            response.delete_cookie('sessionId')
        else:
            response = Response({'details': 'Invalid session token'}, status=status.HTTP_400_BAD_REQUEST)
            
        return response

class CustomerProfileView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated, IsCustomer]
    serializer_class = CustomerProfileSerializer
    
    def get(self, request, *args, **kwargs):
        customer = request.user.customer
        serializer = CustomerProfileSerializer(customer)

        return Response(serializer.data)