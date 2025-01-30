from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from ..models import Renovation
from ..serializers.renovation import RenovationSerializer
from django.shortcuts import get_object_or_404
from django.db.models import Q

class RenovationListView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        supervisor = request.user.supervisor
        customer = request.user.customer

        try:
            renovation = Renovation.objects.filter(
                Q(supervisor=supervisor) | Q(customer=customer)
            )
        except Renovation.DoesNotExist:
            return Response({"details": "Renovation not found"}, status=404)
       
        
        serialized_Renovations = RenovationSerializer(renovation, many=True).data
        return Response(serialized_Renovations)

class RenovationView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, track, *args, **kwargs):
        renovation = get_object_or_404(
            Renovation,
            track=track
        )
        
        serialized_renovation = RenovationSerializer(renovation).data
        return Response(serialized_renovation)