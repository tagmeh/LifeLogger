import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_list_users(api_client, user):
    user = user
    url = reverse('user:list-users')
    api_client.force_authenticate(user)
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data['count'] == 1


def test_user_list_filtering_by_first_name(api_client, user, users):
    api_client.force_authenticate(user)
    url = reverse('user:list-users')
    response = api_client.get(url, {'first_name': 'Alice'})

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['first_name'] == 'Alice'


def test_user_list_filtering_by_is_active(api_client, user, users):
    api_client.force_authenticate(user)
    url = reverse('user:list-users')
    response = api_client.get(url, {'is_active': True})

    assert response.status_code == 200
    assert len(response.data) == 2
    assert all(user['is_active'] for user in response.data)


def test_user_list_filtering_by_first_name_and_is_active(api_client, user, users):
    api_client.force_authenticate(user)
    url = reverse('user:list-users')
    response = api_client.get(url, {'first_name': 'Charlie', 'is_active': False})

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['first_name'] == 'Charlie'
    assert not response.data[0]['is_active']