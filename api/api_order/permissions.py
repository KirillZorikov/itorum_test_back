from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated

from .models import ExportAccess


class HasAccess(permissions.BasePermission):
    def has_permission(self, request, view):
        return ExportAccess.objects.filter(user=request.user).exists()


IsAuthenticatedAndHasAccess = IsAuthenticated & HasAccess
