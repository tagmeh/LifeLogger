import pytest
from habits.models import Habit, SubscribedHabit, HabitHistoryLog


@pytest.mark.django_db
def test_create_habit():
    habit = Habit.objects.create(name='Drink Water', is_good_habit=True)
    assert habit.name == 'Drink Water'
    assert habit.is_good_habit is True


@pytest.mark.django_db
def test_habit_str():
    habit = Habit.objects.create(name='Drink Water', is_good_habit=True)
    assert str(habit) == 'Drink Water Type: Good'


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


@pytest.mark.django_db
def test_habit_history_log_creation(test_user, good_habit):
    user = test_user()
    subscribed_habit = SubscribedHabit.objects.create(user=user, habit=good_habit)
    subscribed_habit.log_progress(achieved=True)

    logs = HabitHistoryLog.objects.all()
    log = logs.first()

    assert SubscribedHabit.objects.all().count() == 1
    assert logs.count() == 1
    assert log.achieved is True
    assert str(log) == f"User {user.email} achieved Habit {good_habit.name} on {log.created_on}: {log.achieved}"
