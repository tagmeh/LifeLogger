from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Habit, UserHabits


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = get_user_model()
#         fields = '__all__'


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'


class UserHabitsSerializer(serializers.ModelSerializer):
    habits = HabitSerializer(many=True)
    # user = UserSerializer(read_only=True)

    class Meta:
        model = UserHabits
        fields = ('user', 'date', 'habits')
        read_only_fields = ('user', 'date')

    def create(self, validated_data):
        habits = validated_data.pop('habits')  # Remove the habits list[dict[]]
        user_habits = UserHabits.objects.create(**validated_data)  # Get a UserHabits instance

        # Get/Create a Habit object, then add it to the M2M field of UserHabits object
        for habit in habits:
            habit, _ = Habit.objects.get_or_create(name__iexact=habit['name'])
            user_habits.habits.add(habit)

        return user_habits

    def update(self, instance, validated_data):
        habits = validated_data.pop('habits')
        instance.user = validated_data.get('user', instance.user)  # TODO: Does this overwrite the existing user?
        instance.save()

        for habit in habits:
            habit, _ = Habit.objects.get_or_create(name__iexact=habit['name'])
            instance.habits.add(habit)

        return instance
