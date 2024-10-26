from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from pharmacy_management_system.medications.models import RefillRequest

from .serializers import RefillRequestSummarySerializer


class PrescriptionSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Get count of requested and filled prescriptions
        requested_count = RefillRequest.objects.filter(status="PENDING").count()
        filled_count = RefillRequest.objects.filter(status="COMPLETED").count()

        summary = {
            "requested_count": requested_count,
            "filled_count": filled_count,
        }
        return Response(summary, status=status.HTTP_200_OK)


class PendingRefillsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        pending_refills = RefillRequest.objects.filter(status="PENDING")
        serializer = RefillRequestSummarySerializer(pending_refills, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CompletedRefillsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Get list of completed refills
        completed_refills = RefillRequest.objects.filter(status="COMPLETED")
        serializer = RefillRequestSummarySerializer(completed_refills, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
