from rest_framework import generics, status
from rest_framework.response import Response
from ..serializers.supervisor import SupervisorLoginSerializer, SupervisorProfileSerializer
from ..models import Session, BlackList
from django.middleware.csrf import get_token
import uuid
from rest_framework import status
from datetime import timedelta
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.utils.timezone import now
from authentication.permissions import IsSupervisor
from ..utils import get_client_ip

class SupervisorLoginView(generics.GenericAPIView):
    serializer_class = SupervisorLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        csrf_token = get_token(request)

        supervisor = serializer.validated_data
        
        blacklisted_ip = BlackList.objects.filter(ip=get_client_ip(request)).first()
            
        if blacklisted_ip:
            return Response({'details': 'Your IP is blacklisted'}, status=status.HTTP_400_BAD_REQUEST)
        
        token = str(uuid.uuid4())
        supervisor.last_login = now()
        supervisor.save()

        expires_at = now() + timedelta(days=2)

        session = Session.objects.create(
            supervisor=supervisor,
            session_token=token,
            ip=get_client_ip(request),
            expires_at=expires_at,
        )
        
        supervisor_data = SupervisorProfileSerializer(supervisor).data
        
        response = Response(supervisor_data, status=status.HTTP_200_OK)
        response.set_cookie(
            'sessionId', session.session_token, expires=expires_at,
            httponly=False,  # Change to True if you don't need JavaScript access
            secure=False,  # Use False in local development
            samesite=None
        )
        response['X-CSRFToken'] = csrf_token
        return response

class SupervisorLogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, IsSupervisor]

    def post(self, request, *args, **kwargs):
        supervisor = request.user.supervisor
        sessions = Session.objects.filter(supervisor_id=supervisor)
        response = Response({'details': 'Logged out successfully'}, status=status.HTTP_200_OK)
        if sessions:
            sessions.delete()
            response.delete_cookie('sessionId')
        else:
            response = Response({'details': 'Invalid session token'}, status=status.HTTP_400_BAD_REQUEST)
            
        return response

class SupervisorProfileView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated, IsSupervisor]
    serializer_class = SupervisorProfileSerializer
    
    def get(self, request, *args, **kwargs):
        supervisor = request.user.supervisor
        serializer = SupervisorProfileSerializer(supervisor)

        return Response(serializer.data)