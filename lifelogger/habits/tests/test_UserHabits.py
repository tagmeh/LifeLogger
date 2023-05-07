from habits.models import UserHabits


def test_user_habits_str(user):
    user_habits = UserHabits.objects.create(user=user)
    assert str(user_habits) == f"{user.username} on {user_habits.date}"
