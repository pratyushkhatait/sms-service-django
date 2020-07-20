from rest_framework.authentication import BasicAuthentication
from rest_framework.exceptions import PermissionDenied
from sms.models import Account


class AuthenticationMixin(BasicAuthentication):
    """
    This is a authentication class, that grants valid users to use the API
    """
    def authenticate_credentials(self, userid, password, request=None):
        try:
            user = Account.objects.get(username=userid, auth_id=password)
        except Account.DoesNotExist:
            raise PermissionDenied
        return user, None
