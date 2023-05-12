import pytest

from pprint import pprint
from django.urls import reverse
from rest_framework import status


def test_list_users(api_client, user):
    user = user()  # Generates 1 user in the database
    url = reverse('user:list-users')
    api_client.force_authenticate(user)
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data['count'] == 1


def test_user_list_filtering_by_first_name(api_client, user, users):
    user = user()
    api_client.force_authenticate(user)
    url = reverse('user:list-users')
    response = api_client.get(url, {'first_name': 'Alice'})

    pprint(response.__dict__)
    pprint(response.data)

    assert response.status_code == 200
    assert len(response.data.results) == 4
    assert response.data.results[0]['first_name'] == 'Alice'


def test_user_list_filtering_by_is_active(api_client, user, users):
    user = user()
    api_client.force_authenticate(user)
    url = reverse('user:list-users')
    response = api_client.get(url, {'is_active': True})

    pprint(response.__dict__)
    pprint(response.data)

    assert response.status_code == 200
    assert len(response.data.results) == 4
    assert all(user['is_active'] for user in response.data)


def test_user_list_filtering_by_first_name_and_is_active(api_client, user, users):
    user = user()
    api_client.force_authenticate(user)
    url = reverse('user:list-users')
    response = api_client.get(url, {'first_name': 'Charlie', 'is_active': False})

    pprint(response.__dict__)
    pprint(response.data)

    assert response.status_code == 200
    assert len(response.data.results) == 4
    assert response.data.results[0]['first_name'] == 'Charlie'
    assert not response.data.results[0]['is_active']
