from typing import Any
from django.contrib.auth import get_user_model, models
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import UserSerializer

User = get_user_model()


@extend_schema(tags=['accounts'])
class UserListAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [BasicAuthentication, JWTAuthentication]
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
        summary='List Accounts',
        operation_id='list-accounts',
    )
    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Query existing Users on the platform.
        """
        return super().get(request, *args, **kwargs)


@extend_schema(tags=['accounts'])
class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []
    authentication_classes = []

    @extend_schema(
        summary='Create Account',
        operation_id='create-accounts',
    )
    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Create a new User. The Email field will be used for the username login (JWT Auth)
        """
        return super().post(request, *args, **kwargs)


@extend_schema(tags=['accounts'])
class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [BasicAuthentication, JWTAuthentication]
    lookup_field = 'pk'

    @extend_schema(methods=['PUT'], exclude=True)  # Excludes it from the Swagger
    def put(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return Response("This method is not allowed", status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @extend_schema(summary='Retrieve Account', operation_id='retrieve-account')
    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Retrieve a single User instance
        """
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary='Update Account',
        operation_id='update-account',
    )
    def patch(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Update a User object.
        """
        return super().patch(request, *args, **kwargs)
