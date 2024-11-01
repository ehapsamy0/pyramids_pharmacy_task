from django_filters import rest_framework as filters
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from users.permissions import IsPatient
from users.permissions import IsPharmacist

from pharmacy_management_system.users.models import Pharmacist

from .filters import RefillRequestFilter
from .models import Medication
from .models import RefillRequest
from .serializers import MedicationSerializer
from .serializers import RefillRequestReadSerializer
from .serializers import RefillRequestSerializer


class MedicationListView(generics.ListCreateAPIView):
    """
    List all available medications. Accessible only by Patients.
    """

    queryset = Medication.objects.all()
    serializer_class = MedicationSerializer
    permission_classes = [permissions.IsAuthenticated, IsPatient]


class RefillRequestCreateView(generics.CreateAPIView):
    """
    Create a new refill request. Accessible only by Patients.
    """

    serializer_class = RefillRequestSerializer
    permission_classes = [permissions.IsAuthenticated, IsPatient]

    def perform_create(self, serializer):
        # Automatically assign the patient from the request's user
        patient = self.request.user.patient_profile
        serializer.save(patient=patient)


class RefillRequestListView(generics.ListAPIView):
    """
    List refill requests.
    - Pharmacists see all refill requests with filters for pending and completed.
    - Patients can see their own refill requests.
    """

    filter_backends = [filters.DjangoFilterBackend]
    permission_classes = [permissions.IsAuthenticated]
    filterset_class = RefillRequestReadSerializer

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return RefillRequestReadSerializer
        return RefillRequestSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_pharmacist:
            # Pharmacist can view all requests
            return RefillRequest.objects.all().select_related("medication")
        else:
            # Patients only view their own requests
            return RefillRequest.objects.filter(patient__user=user).select_related(
                "medication"
            )


class RefillRequestUpdateView(generics.UpdateAPIView):
    """
    Update a refill request to mark it as fulfilled. Accessible only by Pharmacists.
    """

    queryset = RefillRequest.objects.all()
    serializer_class = RefillRequestSerializer
    permission_classes = [permissions.IsAuthenticated, IsPharmacist]

    def update(self, request, *args, **kwargs):
        refill_request = self.get_object()
        if refill_request.is_fulfilled:
            return Response(
                {"detail": "Refill request is already fulfilled."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        refill_request.is_fulfilled = True
        refill_request.status = "COMPLETED"
        refill_request.pharmacist = Pharmacist.objects.get(user=request.user)
        refill_request.save()
        serializer = self.get_serializer(refill_request)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PendingRefillRequestListView(generics.ListAPIView):
    serializer_class = RefillRequestReadSerializer
    permission_classes = [IsPharmacist]

    def get_queryset(self):
        return RefillRequest.objects.filter(status="PENDING")


# Pharmacist view: View completed refill requests
class CompletedRefillRequestListView(generics.ListAPIView):
    serializer_class = RefillRequestReadSerializer
    permission_classes = [IsPharmacist]

    def get_queryset(self):
        return RefillRequest.objects.filter(status="COMPLETED")
