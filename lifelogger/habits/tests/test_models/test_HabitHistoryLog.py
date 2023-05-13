import pytest

from habits.models import SubscribedHabit, HabitHistoryLog


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