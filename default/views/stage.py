from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from ..models import Stage, Service
from ..serializers.stage import StageSerializer
from django.shortcuts import get_object_or_404

class StageListView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, *args, **kwargs):
        serviceId = request.query_params.get('serviceId', None)

        try:
            service = Service.objects.get(id=serviceId)
        except Service.DoesNotExist:
            return Response({"detail": "Service not found"}, status=404)
        
        try:
            stages = Stage.objects.filter(service=service)
        except Stage.DoesNotExist:
            return Response({"detail": "Stage not found"}, status=404)
        
        serialized_stages = StageSerializer(stages, many=True).data
        return Response(serialized_stages)

class StageView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, id, *args, **kwargs):
        stage = get_object_or_404(
            Stage,
            id=id
        )
        
        serialized_stage = StageSerializer(stage).data
        return Response(serialized_stage)