from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied
from sms.models import Account


class ValidationMixin(BasePermission):
    """
    This is a authentication class, that grants valid users to use the API
    """

    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        user_name, password = request.GET["username"], request.GET["password"]
        try:
            Account.objects.get(username=user_name, auth_id=password)
        except Account.DoesNotExist:
            raise PermissionDenied
        return True
