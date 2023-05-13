from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Habit, HabitHistoryLog, SubscribedHabit


class LimitedExtendedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'email')


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'


class SubscribedHabitSerializer(serializers.ModelSerializer):
    habit = HabitSerializer(read_only=True)

    class Meta:
        model = SubscribedHabit
        fields = ('habit', 'updated_today', 'subscribed_on')


class HabitHistoryLogSerializer(serializers.ModelSerializer):
    user = LimitedExtendedUserSerializer(read_only=True)
    habit = HabitSerializer(read_only=True)

    class Meta:
        model = HabitHistoryLog
        fields = ('user', 'habit', 'created_on', 'achieved')


class UpdateHabitsSerializer(serializers.Serializer):
    habit_index = serializers.IntegerField()
    achieved = serializers.BooleanField()


class AddRemoveSubscribedHabitSerializer(serializers.Serializer):
    habit_ids = serializers.ListField(child=serializers.IntegerField())

    def validate_habit_ids(self, habit_ids):
        if len(habit_ids) == 0:  # Doesn't allow payloads with empty arrays.
            raise serializers.ValidationError('Array must not be empty.')

        habit_ids = list(set(habit_ids))  # Remove duplicates.
        return habit_ids
