from typing import Any

from drf_spectacular.utils import extend_schema
from rest_framework import generics, permissions, status
from rest_framework.request import Request
from rest_framework.response import Response

from .models import VitalLog
from .serializers import VitalLogSerializer


class VitalLogCreateListView(generics.ListCreateAPIView):
    serializer_class = VitalLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return VitalLog.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class VitalLogRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = VitalLogSerializer
    permission_classes = {'DELETE': [permissions.IsAuthenticated, permissions.IsAdminUser]}

    def get_permissions(self):
        return self.permission_classes.get(self.request.method.upper(), [permissions.IsAuthenticated])

    def get_queryset(self):
        return VitalLog.objects.filter(user=self.request.user)

    @extend_schema(summary='Retrieve a single Vital Log', operation_id='retrieve-vital-log')
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @extend_schema(methods=['PUT'], exclude=True)  # Excludes it from the Swagger
    def put(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return Response("This method is not allowed", status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @extend_schema(summary='Retrieve a single Vital Log', operation_id='retrieve-vital-log')
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    @extend_schema(summary='Retrieve a single Vital Log', operation_id='retrieve-vital-log')
    def delete(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return self.permission_denied(request)
        return super().delete(request, *args, **kwargs)
