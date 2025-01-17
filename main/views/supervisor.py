from rest_framework import generics, status
from rest_framework.response import Response
from ..serializers.supervisor import LoginSerializer, ProfileSerializer
from ..models import Session
from django.middleware.csrf import get_token
import uuid
from rest_framework import status
from datetime import timedelta
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.utils.timezone import now


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        csrf_token = get_token(request)

        supervisor = serializer.validated_data

        token = str(uuid.uuid4())
        supervisor.last_login = now()
        supervisor.save()

        expires_at = now() + timedelta(days=2)

        session = Session.objects.create(
            supervisor=supervisor,
            session_token=token,
            expires_at=expires_at,
        )
        
        supervisor_data = ProfileSerializer(supervisor).data
        
        response = Response(supervisor_data, status=status.HTTP_200_OK)
        response.set_cookie(
            'sessionId',
            session.session_token,
            expires=expires_at, 
        )
        response['X-CSRFToken'] = csrf_token
        return response

class LogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        supervisor = request.user
        sessions = Session.objects.filter(supervisor_id=supervisor)
        response = Response({'details': 'Logged out successfully'}, status=status.HTTP_200_OK)
        if sessions:
            sessions.delete()
            response.delete_cookie('sessionId')
        else:
            response = Response({'details': 'Invalid session token'}, status=status.HTTP_400_BAD_REQUEST)
            
        return response

class ProfileView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer
    
    def get(self, request, *args, **kwargs):
        supervisor = request.user
        serializer = ProfileSerializer(supervisor)

        return Response(serializer.data)