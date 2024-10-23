from rest_framework import serializers
from .models import Medication, RefillRequest
from pharmacy_management_system.users.models import Patient, Pharmacist


class MedicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medication
        fields = ["id", "name", "description", "quantity_available"]


class RefillRequestSerializer(serializers.ModelSerializer):
    patient = serializers.StringRelatedField(read_only=True)
    medication = serializers.PrimaryKeyRelatedField(queryset=Medication.objects.all())

    class Meta:
        model = RefillRequest
        fields = [
            "id",
            "patient",
            "medication",
            "quantity_requested",
            "request_date",
            "is_fulfilled",
            "pharmacist",
        ]
        read_only_fields = ["request_date", "is_fulfilled", "pharmacist"]

    def create(self, validated_data):
        user = self.context["request"].user
        patient = Patient.objects.get(user=user)
        refill_request = RefillRequest.objects.create(patient=patient, **validated_data)
        # Optionally, log the action
        from audit_logs.models import AuditLog

        AuditLog.objects.create(
            user=user,
            action="MEDICATION_REQUEST",
            description=f"Requested {validated_data['quantity_requested']} of {validated_data['medication'].name}",  # noqa: E501
        )
        return refill_request


