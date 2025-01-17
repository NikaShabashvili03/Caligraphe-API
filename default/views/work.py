from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from ..models import Work
from ..serializers.work import WorkSerializer
from django.shortcuts import get_object_or_404

class WorkListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        try:
            works = Work.objects.all()
        except Work.DoesNotExist:
            return Response({"detail": "Work not found"}, status=404)
        
        serialized_works = WorkSerializer(works, many=True).data
        return Response(serialized_works)

class WorkView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, id, *args, **kwargs):
        work = get_object_or_404(
            Work,
            id=id
        )
        
        serialized_work = WorkSerializer(work).data
        return Response(serialized_work)