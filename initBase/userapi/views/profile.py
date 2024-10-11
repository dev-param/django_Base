from .base import MainAPIView
from rest_framework.response import Response

from userapi.models import XAuth


class ProfileAPIView(MainAPIView):
    def post(self, request):
        ic(XAuth.active.through.objects.filter(user__id=1))

        return Response({})