import pytest
from django.contrib.auth import get_user_model
from datetime import date
from habits.models import UserHabits
from habits.serializers import UserHabitsSerializer

User = get_user_model()


@pytest.mark.django_db
def test_UserHabitsSerializer_create(user, habits_data, good_habit, bad_habit):
    """
    Happy Path. Test if everything works as expected.
    Create a UserHabit, attach two Habits, and save to the database.
    """
    serializer_data = {'user': user.id, 'habits': habits_data}
    serializer = UserHabitsSerializer(data=serializer_data)
    assert serializer.is_valid(raise_exception=True)

    user_habits = serializer.save(user=user)

    assert user_habits.user == user
    assert user_habits.date == date.today()
    assert user_habits.habits.count() == 2
    assert good_habit in user_habits.habits.all()
    assert bad_habit in user_habits.habits.all()


def test_UserHabitsSerializer_create_with_non_existing_habit(user):
    """
    Create a UserHabit instance with a Habit that didn't exist prior.
    """
    serializer_data = {'user': user.id, 'habits': [{'name': 'non-existing habit'}]}
    serializer = UserHabitsSerializer(data=serializer_data)

    serializer.is_valid(raise_exception=True)

    user_habits = serializer.save(user=user)

    assert user_habits.habits.count() == 1


@pytest.mark.django_db
def test_user_habit_serializer_update(user, habits_data, good_habit, bad_habit):
    """ """
    # Create a user habit instance
    user_habit = UserHabits.objects.create(user=user)

    # Update the user habit instance
    updated_data = {'habits': habits_data}
    updated_serializer = UserHabitsSerializer(user_habit, data=updated_data, partial=True)
    updated_serializer.is_valid(raise_exception=True)
    updated_user_habit = updated_serializer.save()

    updated_user_habit.refresh_from_db()  # Update the local instance with the database data to be certain.

    # Check that the updated user habit instance has the correct habits
    assert good_habit in updated_user_habit.habits.all()
    assert bad_habit in updated_user_habit.habits.all()
