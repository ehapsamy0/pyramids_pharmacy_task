from django.urls import path

from .views import AdminSummaryView
from .views import CompletedRefillsView
from .views import MonthlyRefillRequestCountView
from .views import MonthlyUserRegistrationCountView
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
    path(
        "refill-requests/monthly-count/",
        MonthlyRefillRequestCountView.as_view(),
        name="monthly-refill-request-count",
    ),
    path('admin-summary/', AdminSummaryView.as_view(), name='admin-summary'),
    path(
        "user-registration-count/",
        MonthlyUserRegistrationCountView.as_view(),
        name="user-registration-count",
    ),
]
