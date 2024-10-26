from django.urls import path

from .views import CompletedRefillsView
from .views import PendingRefillsView
from .views import PrescriptionSummaryView

urlpatterns = [
    path(
        "prescription-summary/",
        PrescriptionSummaryView.as_view(),
        name="prescription-summary",
    ),
    path("pending-refills/", PendingRefillsView.as_view(), name="pending-refills"),
    path(
        "completed-refills/", CompletedRefillsView.as_view(), name="completed-refills"
    ),
]
