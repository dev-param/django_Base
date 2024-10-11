from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import APIException, _get_error_details
from rest_framework import status

class CustomAPIX(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('Something went Wrong!')
    default_code = 'invalid'

    def __init__(self, detail=None, code=None, statusCode=None, server_error=False):
        if server_error:
            self.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        if detail is None:
            detail = self.default_detail
        if code is None:
            code = self.default_code
        if statusCode is not None:
            self.status_code = statusCode
        
        # For validation failures, we may collect many errors together,
        # so the details should always be coerced to a list if not already.
        if isinstance(detail, tuple):
            detail = list(detail)
        elif not isinstance(detail, dict) and not isinstance(detail, list):
            detail = [detail]

        self.detail = _get_error_details(detail, code)