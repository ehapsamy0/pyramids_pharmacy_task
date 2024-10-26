from django_filters import rest_framework as filters
from .models import RefillRequest


class RefillRequestFilter(filters.FilterSet):
    status = filters.ChoiceFilter(
        choices=RefillRequest.STATUS_CHOICES
    )  # Filter for status field

    class Meta:
        model = RefillRequest
        fields = ["status"]
