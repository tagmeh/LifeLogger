import logging
from typing import Any
from urllib.request import Request

from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework.authentication import BasicAuthentication
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, ListAPIView, UpdateAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication

from habits.models import Habit, SubscribedHabit, HabitHistoryLog
from habits.serializers import (
    HabitSerializer,
    SubscribedHabitSerializer,
    UpdateHabitsSerializer,
    HabitHistoryLogSerializer,
    AddRemoveSubscribedHabitSerializer,
)
from lifelogger.custom_APIView import UpdateCreateAPIView

log = logging.getLogger(__name__)


@extend_schema(tags=['Habits'])
class HabitListCreateAPIView(ListCreateAPIView):
    """Expose the List (GET) and Create (POST) endpoints for the Habits model."""

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [BasicAuthentication, JWTAuthentication]

    @extend_schema(summary='List Habits', operation_id='list-habits')
    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Get a list of Habit objects"""
        log.debug('Getting a list of Habits')
        return super().get(request, *args, **kwargs)

    @extend_schema(summary='Create a Habit', operation_id='create-habit')
    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Create a new Habit"""
        log.debug('Creating a new Habit')
        return super().post(request, *args, **kwargs)


@extend_schema(tags=['Habits'])
class HabitUpdateDetailAPIView(RetrieveUpdateAPIView):
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


@extend_schema(tags=['Subscribed Habits'])
class SubscribedHabitsListAPIView(ListAPIView):
    queryset = SubscribedHabit.objects.all()
    serializer_class = SubscribedHabitSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [BasicAuthentication, JWTAuthentication]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['habit__id', 'habit__name']
    filterset_fields = {
        'id': ['exact'],
        'habit__id': ['exact'],
        'habit__name': ['exact', 'icontains'],
        'updated_today': ['exact'],
        'subscribed_on': ['gte', 'lte'],
    }

    @extend_schema(summary='List Subscribed Habits per User', operation_id='list-subscribed-habits')
    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Displays a list of Habits the current user is subscribed to.

        "Subscribed_on" is a datetime object in the format of YYYY-MM-DD and/or YYYY-MM-DDTHH:MM:SS.ms
        """
        # Add the filter to return only SubscribedHabits for the requesting user.
        self.queryset = self.queryset.filter(user=self.request.user)
        return super().get(request, *args, **kwargs)


@extend_schema(tags=['Subscribed Habits'])
class SubscribedHabitsUpdateAPIView(UpdateAPIView):
    queryset = SubscribedHabit.objects.all()
    serializer_class = UpdateHabitsSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [BasicAuthentication, JWTAuthentication]

    @extend_schema(methods=['PUT'], exclude=True)  # Excludes it from the Swagger
    def put(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return Response("This method is not allowed", status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @extend_schema(
        summary='Modify one or more Subscribed Habits',
        operation_id='modify-subscribed-habits',
        request=UpdateHabitsSerializer(many=True),
    )
    def patch(self, request, *args, **kwargs):
        """
        This view updates the updated_today field and creates a HabitHistoryLog entry
        """
        data = request.data
        serializer = UpdateHabitsSerializer(data=data, many=True)

        if not serializer.is_valid(raise_exception=True):
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        for item in serializer.validated_data:
            with transaction.atomic():
                subbed_hab = SubscribedHabit.objects.get(user=request.user, habit=item['habit_index'])

                # Updates the SubscribedHabit.updated_today to True, and creates a HabitHistoryLog
                subbed_hab.log_progress(achieved=item['achieved'])

        return Response(status=status.HTTP_200_OK)


@extend_schema(tags=['Subscribed Habits'])
class SubscribeHabitsAPIView(UpdateAPIView):
    queryset = SubscribedHabit.objects.all()
    serializer_class = AddRemoveSubscribedHabitSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [BasicAuthentication, JWTAuthentication]

    @extend_schema(methods=['PUT'], exclude=True)  # Excludes it from the Swagger
    def put(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return Response("This method is not allowed", status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @extend_schema(
        summary='Adds one or more Habit(s) to a User',
        operation_id='add-subscribed-habits',
        request=AddRemoveSubscribedHabitSerializer,
    )
    def patch(self, request, *args, **kwargs):
        """
        This endpoint allows a user to "subscribe" to a habit. Will automatically add all Habit ids to the current
        user. Users subscribing to habits is tracked in the intermediary model "SubscribedHabit" for reporting purposes.

        Will wilently ignore any id passed in that doesn't match an existing habit.
        Silently ignores duplicates (You cannot be assigned to the same Habit multiple times).

        Because this is a partial update, you cannot remove habits from the user with this endpoint, in the same vein,
        you do not have to pass in all user habits in order to make this call. Simply adding the new, unsubscribed,
        habit to the payload will add it to the user without affecting the existing habits.
        """
        serializer = AddRemoveSubscribedHabitSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            # The .exclude() avoids re-subscribing to an existing habit and keeps the response message accurate.
            habits = Habit.objects.filter(pk__in=serializer.data['habit_ids']).exclude(
                extendeduser__habits__in=request.user.habits.all()
            )

            if len(habits) == 0:
                response = {'message': f'User is already subscribed to those habits.'}
            else:
                request.user.habits.add(*habits)
                response = {'message': f'User subscribed to {len(habits)} habit(s) successfully'}

            return Response(response, status=status.HTTP_200_OK)
        else:
            response = {'error': serializer.errors}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['Subscribed Habits'])
class UnsubscribeHabitsAPIView(CreateAPIView):
    queryset = SubscribedHabit.objects.all()
    serializer_class = AddRemoveSubscribedHabitSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [BasicAuthentication, JWTAuthentication]

    @extend_schema(
        summary='Remove one or more Habit(s) from the User',
        operation_id='remove-subscribed-habits',
        request=AddRemoveSubscribedHabitSerializer,
    )
    def post(self, request, *args, **kwargs):
        """
        The opposite of the Patch endpoint, this endpoint will remove the association with the given Habit id and the
        user calling the endpoint. In other words, this endpoint allows the user to "unsubscribe"
        from a Habit or habits. (formerly

        Similar to the above endpoint, only habits passed in are removed, won't fail if it attempts to remove habits
        that don't exist, aren't subscribed to, or are duplicates.
        """
        serializer = AddRemoveSubscribedHabitSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            habits = request.user.habits.filter(pk__in=serializer.data['habit_ids'])

            if len(habits) == 0:
                response = {'message': f'User is not subscribed to any of those habits.'}
            else:
                request.user.habits.remove(*habits)
                response = {'message': f'User unsubscribed from {len(habits)} habit(s) successfully'}

            return Response(response, status=status.HTTP_200_OK)
        else:
            response = {'error': serializer.errors}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['Habit History Log'])
class HabitHistoryLogListAPIView(ListAPIView):
    queryset = HabitHistoryLog.objects.all()
    serializer_class = HabitHistoryLogSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [BasicAuthentication, JWTAuthentication]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['habit__id', 'habit__name']
    filterset_fields = {'id': ['exact'], 'habit__id': ['exact'], 'habit__name': ['exact', 'icontains']}

    @extend_schema(summary='List Habit History Log', operation_id='list-habit-history-log')
    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """"""
        # Add the filter to return only SubscribedHabits for the requesting user.
        self.queryset = self.queryset.filter(user=self.request.user)
        return super().get(request, *args, **kwargs)
