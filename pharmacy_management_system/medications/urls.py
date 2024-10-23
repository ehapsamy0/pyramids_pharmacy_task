from django.urls import path

from .views import CompletedRefillRequestListView
from .views import MedicationListView
from .views import PendingRefillRequestListView
from .views import RefillRequestCreateView
from .views import RefillRequestListView
from .views import RefillRequestUpdateView

urlpatterns = [
    path("medications/", MedicationListView.as_view(), name="medication-list"),
    path(
        "refill-requests/", RefillRequestListView.as_view(), name="refill-request-list"
    ),
    path(
        "refill-requests/create/",
        RefillRequestCreateView.as_view(),
        name="refill-request-create",
    ),
    path(
        "refill-requests/<int:pk>/fulfill/",
        RefillRequestUpdateView.as_view(),
        name="refill-request-fulfill",
    ),
    # Pharmacist endpoints
    path(
        "refill-requests/pending/",
        PendingRefillRequestListView.as_view(),
        name="pending-refill-requests",
    ),
    path(
        "refill-requests/completed/",
        CompletedRefillRequestListView.as_view(),
        name="completed-refill-requests",
    ),
]
