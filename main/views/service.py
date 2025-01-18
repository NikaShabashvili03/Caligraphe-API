from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from ..models import Service
from ..serializers.service import ServiceSerializer
from django.shortcuts import get_object_or_404


class ServiceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id, *args, **kwargs):
        supervisor = request.user
        
        service = get_object_or_404(
            Service.objects.filter(renovation__supervisor=supervisor, id=id)
        )
        
        serialized_service = ServiceSerializer(service).data
        return Response(serialized_service)