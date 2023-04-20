from typing import Any
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListCreateAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from .serializers import UserSerializer

User = get_user_model()


class UserListCreateAPIView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['first_name', 'last_name', 'username', 'email']
    filterset_fields = {
        'id': ['exact'],
        'first_name': ['exact', 'icontains'],
        'last_name': ['exact', 'icontains'],
        'username': ['exact', 'icontains'],
        'email': ['exact', 'icontains'],
        'is_active': ['exact'],
    }

    @extend_schema(
        parameters=[OpenApiParameter('search', str)],
        responses=UserSerializer(many=True),
        tags=['accounts'],
        summary='List Accounts',
        operation_id='get-accounts'
    )
    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Query existing Users on the platform.
        """
        return super().get(request, *args, **kwargs)

    @extend_schema(
        tags=['accounts'],
        summary='Create Account',
        operation_id='create-accounts'
    )
    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Create a new User.
        """
        return super().post(request, *args, **kwargs)
