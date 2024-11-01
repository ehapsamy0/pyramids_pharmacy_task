from django.contrib.auth import get_user_model
from django.db.models import Count
from django.db.models.functions import TruncMonth
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from pharmacy_management_system.medications.models import Medication
from pharmacy_management_system.medications.models import RefillRequest
from pharmacy_management_system.medications.models import RefillRequest
from pharmacy_management_system.users.models import Patient
from pharmacy_management_system.users.models import Pharmacist
from pharmacy_management_system.users.models import User

from .serializers import RefillRequestSummarySerializer

User = get_user_model()


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


class MonthlyRefillRequestCountView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Group refill requests by month and count them
        monthly_data = (
            RefillRequest.objects.annotate(month=TruncMonth("request_date"))
            .values("month")
            .annotate(count=Count("id"))
            .order_by("month")
        )

        # Format data for easier consumption in frontend
        result = [
            {"month": item["month"].strftime("%Y-%m"), "count": item["count"]}
            for item in monthly_data
        ]

        return Response(result)


class MonthlyUserRegistrationCountView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        # Group by month and count users
        monthly_counts = (
            User.objects.annotate(month=TruncMonth("date_joined"))
            .values("month")
            .annotate(count=Count("id"))
            .order_by("month")
        )

        # Format data for the response
        data = [
            {
                "month": item["month"].strftime("%B %Y"),  # e.g., "August 2024"
                "count": item["count"],
            }
            for item in monthly_counts
        ]

        return Response(data)


class AdminSummaryView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        # Count total users
        total_users = User.objects.count()
        total_patients = Patient.objects.count()
        total_pharmacists = Pharmacist.objects.count()

        # Count total medications
        total_medications = Medication.objects.count()

        # Count refill requests by status
        pending_refills = RefillRequest.objects.filter(status="PENDING").count()
        completed_refills = RefillRequest.objects.filter(status="COMPLETED").count()

        # Prepare response data
        data = {
            "total_users": total_users,
            "total_patients": total_patients,
            "total_pharmacists": total_pharmacists,
            "total_medications": total_medications,
            "pending_refills": pending_refills,
            "completed_refills": completed_refills,
        }

        return Response(data)
