from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from ..models import Stage, Work
from ..serializers.stage import StageSerializer
from django.db.models import F
from django.utils import timezone

class StageListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        work_id = request.query_params.get('workId')

        if not work_id:
            return Response({"detail": "workId query parameter is required."}, status=400)

        try:
            work = Work.objects.get(id=work_id)
        except Work.DoesNotExist:
            return Response({"detail": "Work not found."}, status=404)

        stages = Stage.objects.filter(work=work).order_by(F('is_completed').asc(nulls_last=True))

        serialized_stages = StageSerializer(stages, many=True).data
        return Response(serialized_stages)
    

class StageCompleteView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, id, *args, **kwargs):
        supervisor = request.user

        try:
            stage = Stage.objects.get(id=id, work__renovation__supervisor=supervisor)
        except Stage.DoesNotExist:
            return Response({"detail": "Stage not found or you does not have access"}, status=404)

        if stage.is_completed == None:
            stage.is_completed = timezone.now()
        else:
            stage.is_completed = None
        
        stage.save()

        serialized_stage = StageSerializer(stage).data
        return Response(serialized_stage)