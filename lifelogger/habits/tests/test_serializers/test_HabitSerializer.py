import pytest

from rest_framework.exceptions import ValidationError

from habits.serializers import HabitSerializer


# Habit Serializer
@pytest.mark.django_db
def test_create_habit_empty_name():
    payload = {'name': '', 'is_good_habit': True}
    serializer = HabitSerializer(data=payload)

    with pytest.raises(ValidationError):
        serializer.is_valid(raise_exception=True)


@pytest.mark.django_db
def test_create_habit_name_too_long():
    payload = {'name': 'a' * 51, 'is_good_habit': True}
    serializer = HabitSerializer(data=payload)

    with pytest.raises(ValidationError):
        serializer.is_valid(raise_exception=True)