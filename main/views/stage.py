from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from authentication.permissions import IsSupervisor
from ..models import Stage, Service
from ..serializers.stage import StageSerializer
from django.db.models import F
from django.utils import timezone

class StageListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        service_id = request.query_params.get('serviceId')

        if not service_id:
            return Response({"details": "serviceId query parameter is required."}, status=400)

        try:
            service = Service.objects.get(id=service_id)
        except Service.DoesNotExist:
            return Response({"details": "Service not found."}, status=404)

        stages = Stage.objects.filter(service=service).order_by(F('is_completed').asc(nulls_last=True))

        serialized_stages = StageSerializer(stages, many=True).data
        return Response(serialized_stages)
    

class StageCompleteView(APIView):
    permission_classes = [IsAuthenticated, IsSupervisor]

    def patch(self, request, id, *args, **kwargs):
        supervisor = request.user.supervisor

        try:
            stage = Stage.objects.get(id=id, service__renovation__supervisor=supervisor)
        except Stage.DoesNotExist:
            return Response({"details": "Stage not found or you does not have access"}, status=404)

        if stage.is_completed == None:
            stage.is_completed = timezone.now()
        else:
            stage.is_completed = None
        
        stage.save()

        serialized_stage = StageSerializer(stage).data
        return Response(serialized_stage)