from rest_framework import generics, status
from rest_framework.response import Response
from authentication.serializers.customer import CustomerResetPasswordSerializer, SendCustomerResetPasswordSerializer, CustomerLoginSerializer, CustomerProfileSerializer, CustomerRegisterSerializer, SendCustomerVerificationEmailSerializer
from ..models.session import Session, Customer
from django.middleware.csrf import get_token
import uuid
from rest_framework import status
from datetime import timedelta
from rest_framework.permissions import AllowAny, IsAuthenticated
from authentication.permissions import IsCustomer
from django.utils.timezone import now


import jwt
from rest_framework.views import APIView
from authentication.utils import verify_google_token
import requests

from django.utils import timezone
from django.conf import settings

from django.template.loader import render_to_string
from django.core.mail import send_mail

from rest_framework.exceptions import PermissionDenied

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
            'sessionId', session.session_token, expires=expires_at, 
            samesite='None', secure=True
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
        
        response = Response(customer_data, status=status.HTTP_201_CREATED)
        response.set_cookie(
            'sessionId', session.session_token, expires=expires_at, 
            samesite='Strict', secure=True
        )
        csrf_token = get_token(request)
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

class GoogleLogin(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        token = request.data.get("token")
        if not token:
            return Response({"error": "Token is missing"}, status=400)

        try:
            decoded_token = verify_google_token(token)

            email = decoded_token.get("email")
            firstname = decoded_token.get("given_name", "")
            lastname = decoded_token.get("family_name", "")

            if not email:
                return Response({"error": "Email is missing from the token"}, status=400)

            user, created = Customer.objects.get_or_create(email=email)

            if created:
                user.firstname = firstname
                user.lastname = lastname
                user.email_verified = now()
                user.set_password(uuid.uuid4().hex)
                user.save()

            session_token = str(uuid.uuid4())
            expires_at = now() + timedelta(days=2)

            session = Session.objects.create(
                customer=user,
                session_token=session_token,
                expires_at=expires_at
            )

            customer_data = CustomerProfileSerializer(user).data
        
            response = Response(customer_data, status=status.HTTP_200_OK)
            response.set_cookie(
                'sessionId', session.session_token, expires=expires_at, 
                samesite='None', secure=True
            )

            return response

        except jwt.ExpiredSignatureError:
            return Response({"error": "Token has expired"}, status=400)
        except jwt.DecodeError:
            return Response({"error": "Invalid token"}, status=400)
        except requests.exceptions.RequestException as e:
            return Response({"error": f"Error fetching Google's public keys: {str(e)}"}, status=400)
        except Exception as e:
            return Response({"error": str(e)}, status=400)
        

class CustomerVerificationEmail(APIView):
    def get(self, request, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get("user_id")

            customer = Customer.objects.filter(pk=user_id).first()
            if not customer:
                return Response({"details": "Customer does not exist."}, status=status.HTTP_404_NOT_FOUND)

            if customer.email_verified:
                return Response({"details": "Email is already verified."}, status=status.HTTP_200_OK)

            customer.email_verified = timezone.now()
            customer.save()

            return Response({"details": "Email successfully verified."}, status=status.HTTP_200_OK)

        except jwt.ExpiredSignatureError:
            return Response({"details": "The verification link has expired."}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.DecodeError:
            return Response({"details": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"details": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class CustomerSendVerificationEmail(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = SendCustomerVerificationEmailSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            customer = Customer.objects.get(email=email)

            payload = {
                "user_id": str(customer.id),
                "exp": now() + timedelta(minutes=5),
                "iat": now()
            }

            token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

            verification_url = f"{settings.FRONTEND_URL}/verify-email?token={token}"

            email_subject = "Verify your email address"
            email_body = render_to_string('registration/verification_email.html', {
                'user': customer,
                'verification_url': verification_url,
            })

            send_mail(
                email_subject,
                email_body,
                settings.DEFAULT_FROM_EMAIL,
                [customer.email],
            )

            return Response({"details": "Verification email sent successfully."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomerSendResetPassword(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = SendCustomerResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            customer = Customer.objects.get(email=email)

            payload = {
                "user_id": str(customer.id),
                "exp": now() + timedelta(minutes=5),
                "iat": now()
            }

            token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

            reset_url = f"{settings.BACKEND_URL}/api/v3/customer/reset-password/{token}"

            email_subject = "Reset password"
            email_body = render_to_string('registration/reset_password.html', {
                'user': customer,
                'reset_url': reset_url,
            })

            send_mail(
                email_subject,
                email_body,
                settings.DEFAULT_FROM_EMAIL,
                [customer.email],
            )

            return Response({"details": "Url for reset password sent successfully."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomerResetPassword(APIView):
    def post(self, request, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get("user_id")

            if not user_id:
                return Response({"error": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)

            customer = Customer.objects.filter(pk=user_id).first()
            if not customer:
                return Response({"error": "Customer does not exist."}, status=status.HTTP_404_NOT_FOUND)

            serializer = CustomerResetPasswordSerializer(data=request.data)
            if serializer.is_valid():
                password = serializer.validated_data['password']
                customer.set_password(password)
                customer.save()
                return Response({"details": "Password successfully reset."}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except jwt.ExpiredSignatureError:
            return Response({"error": "The token has expired."}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.DecodeError:
            return Response({"error": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)