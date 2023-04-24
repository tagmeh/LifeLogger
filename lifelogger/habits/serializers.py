from rest_framework import serializers
from .models import Habit, UserHabits


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'


class UserHabitsSerializer(serializers.ModelSerializer):
    habits = HabitSerializer(many=True)

    class Meta:
        model = UserHabits
        fields = '__all__'

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