import pytest

from pytest_factoryboy import register

from main.tests.factories import UserFactory

register(UserFactory)  # Access via "user_factory"

