import pytest
from habits.models import SubscribedHabit


@pytest.mark.django_db
def test_subscribed_habit_creation(test_user, habit):
    user = test_user()
    subscribed_habit = SubscribedHabit.objects.create(user=user, habit=habit)

    assert SubscribedHabit.objects.all().count() == 1
    assert (
        str(subscribed_habit)
        == f"User {subscribed_habit.user.email} subscribed to Habit '{subscribed_habit.habit.name}' on {subscribed_habit.subscribed_on}"
    )
    assert subscribed_habit.updated_today is False
