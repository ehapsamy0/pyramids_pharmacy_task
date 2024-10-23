from rest_framework.permissions import BasePermission

class IsPatient(BasePermission):
    """
    Custom permission to only allow access to patients.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_patient)


class IsPharmacist(BasePermission):
    """
    Custom permission to only allow access to pharmacists.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_pharmacist)
