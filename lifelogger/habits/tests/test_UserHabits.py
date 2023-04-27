import pytest
from django.contrib.auth import get_user_model

from habits.models import UserHabits

User = get_user_model()


@pytest.fixture
def user(db):
    return User.objects.create_user(username='testuser', email='test@example.com', password='testpass')


def test_user_habits_str(user):
    user_habits = UserHabits.objects.create(user=user)
    assert str(user_habits) == f"{user.username} on {user_habits.date}"
