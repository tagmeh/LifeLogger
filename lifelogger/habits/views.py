from typing import Any
from urllib.request import Request

from drf_spectacular.utils import extend_schema
from rest_framework.authentication import BasicAuthentication
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Habit, UserHabits
from .serializers import HabitSerializer, UserHabitsSerializer


@extend_schema(tags=['habits'], summary='SUMMARY')
class HabitListAPIView(ListCreateAPIView):
    """Expose the List (GET) and Create (POST) endpoints for the Habits model."""

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [BasicAuthentication, JWTAuthentication]

    @extend_schema(summary='List Habits', operation_id='list-habits')
    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Get a list of Habit objects"""
        return super().get(request, *args, **kwargs)

    @extend_schema(summary='Create a Habit', operation_id='create-habit')
    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Create a new Habit"""
        return super().post(request, *args, **kwargs)


@extend_schema(tags=['habits'])
class HabitDetailAPIView(RetrieveUpdateAPIView):
    """Expose the Retrieve (GET) and the Update (Patch) endpoints for the Habits model."""

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [BasicAuthentication, JWTAuthentication]
    lookup_field = 'pk'

    @extend_schema(methods=['PUT'], exclude=True)  # Excludes it from the Swagger
    def put(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return Response("This method is not allowed", status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @extend_schema(summary='Retrieve a Habit', operation_id='retrieve-habit')
    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Retrieve a single instance of Habit by database id (pk)."""
        return super().get(request, *args, **kwargs)

    @extend_schema(summary='Modify a Habit', operation_id='modify-habit')
    def patch(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Update an existing instance of Habit based on database id (pk)."""
        return super().patch(request, *args, **kwargs)


@extend_schema(tags=['user-habits'])
class UserHabitsListCreateAPIView(ListCreateAPIView):
    """
    List all user habits or create a new UserHabit.
    """

    serializer_class = UserHabitsSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [BasicAuthentication, JWTAuthentication]

    def get_queryset(self):
        return UserHabits.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @extend_schema(summary='List UserHabits', operation_id='list-user-habits')
    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Get a list of UserHabit objects"""
        return super().get(request, *args, **kwargs)

    @extend_schema(summary='Create a UserHabit', operation_id='create-user-habit')
    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Create a new UserHabit object"""
        return super().post(request, *args, **kwargs)


@extend_schema(tags=['user-habits'])
class UserHabitsDetailAPIView(RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a UserHabit object.
    """

    queryset = UserHabits.objects.all()
    serializer_class = UserHabitsSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [BasicAuthentication, JWTAuthentication]
    lookup_field = 'id'

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    @extend_schema(methods=['PUT'], exclude=True)  # Excludes it from the Swagger
    def put(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return Response("This method is not allowed", status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @extend_schema(summary='Retrieve a UserHabit', operation_id='retrieve-user-habit')
    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Retrieve a single instance of UserHabit by database id (pk)."""
        return super().get(request, *args, **kwargs)

    @extend_schema(summary='Modify a UserHabit', operation_id='modify-user-habit')
    def patch(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Update an existing instance of UserHabit based on database id (pk)."""
        return super().patch(request, *args, **kwargs)

    @extend_schema(summary='Delete a UserHabit', operation_id='delete-user-habit')
    def delete(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Delete an instance of UserHabit"""
        return super().delete(request, *args, **kwargs)
