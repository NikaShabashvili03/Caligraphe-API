from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from ..models import Work
from ..serializers.work import WorkSerializer
from django.shortcuts import get_object_or_404


class WorkView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id, *args, **kwargs):
        supervisor = request.user
        
        work = get_object_or_404(
            Work.objects.filter(renovation__supervisor=supervisor, id=id)
        )
        
        serialized_work = WorkSerializer(work).data
        return Response(serialized_work)