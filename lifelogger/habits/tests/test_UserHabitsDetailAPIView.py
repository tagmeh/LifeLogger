from django.urls import reverse
from rest_framework import status

import pytest
from habits.models import Habit


@pytest.mark.django_db
def test_list_habits(api_client, habit, user):
    url = reverse('habits:habit-create-list')
    api_client.force_authenticate(user)
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data['results'][0]['name'] == habit.name
    assert response.data['results'][0]['is_good_habit'] == habit.is_good_habit


@pytest.mark.django_db
def test_create_habit(api_client, habit_data, user):
    url = reverse('habits:habit-create-list')
    api_client.force_authenticate(user)
    response = api_client.post(url, data=habit_data)

    assert response.status_code == status.HTTP_201_CREATED
    habit = Habit.objects.first()
    assert habit.name == habit_data['name']
    assert habit.is_good_habit == habit_data['is_good_habit']
