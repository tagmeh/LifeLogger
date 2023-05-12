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
def test_create_habit(api_client, habit_object, user):
    url = reverse('habits:habit-create-list')
    api_client.force_authenticate(user)
    response = api_client.post(url, data=habit_object)

    assert response.status_code == status.HTTP_201_CREATED
    habit = Habit.objects.first()
    assert habit.name == habit_object['name']
    assert habit.is_good_habit == habit_object['is_good_habit']
