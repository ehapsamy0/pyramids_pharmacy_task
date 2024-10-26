from rest_framework import serializers

from pharmacy_management_system.medications.models import RefillRequest


class RefillRequestSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = RefillRequest
        fields = [
            "id",
            "medication",
            "patient",
            "quantity_requested",
            "status",
            "request_date",
            "is_fulfilled",
        ]
