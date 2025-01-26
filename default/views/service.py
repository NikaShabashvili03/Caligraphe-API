from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from ..models import Service
from ..serializers.service import ServiceSerializer
from django.shortcuts import get_object_or_404

class ServiceListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        try:
            services = Service.objects.all()
        except Service.DoesNotExist:
            return Response({"details": "Service not found"}, status=404)
        
        serialized_services = ServiceSerializer(services, many=True).data
        return Response(serialized_services)

class ServiceView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, id, *args, **kwargs):
        service = get_object_or_404(
            Service,
            id=id
        )
        
        serialized_service = ServiceSerializer(service).data
        return Response(serialized_service)