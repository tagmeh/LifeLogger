import pytest
from rest_framework.test import APIClient

from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    def create_user(username="testuser", email="test@example.com", password="testpass"):
        return User.objects.create_user(username=username, email=email, password=password)

    return create_user


@pytest.fixture
def valid_user_data():
    return {
        "email": "test@example.com",
        "password": "strongpassword",
        "confirm_password": "strongpassword",
        "first_name": "Test",
        "last_name": "User",
    }


@pytest.fixture
def users(user):
    return [
        user(username="Alice", first_name='Alice', is_active=True),
        user(username="Bob", first_name='Bob', is_active=True),
        user(username="Charlie", first_name='Charlie', is_active=True),
        user(username="David", first_name='David', is_active=True),
    ]
