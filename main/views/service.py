from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..models import Service
from ..serializers.service import ServiceSerializer
from django.shortcuts import get_object_or_404
from django.db.models import Q

class ServiceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id, *args, **kwargs):
        supervisor = request.user.supervisor
        customer = request.user.customer


        service = get_object_or_404(
            Service,
            Q(renovation__supervisor=supervisor) | Q(renovation__customer=customer),
            id=id
        )
        
        print(service)
        serialized_service = ServiceSerializer(service).data

        print(serialized_service)
        return Response(serialized_service)