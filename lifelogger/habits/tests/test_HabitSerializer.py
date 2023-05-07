import pytest


@pytest.mark.django_db
def test_habit_serializer_with_valid_data(habit_serializer):
    assert habit_serializer.is_valid(raise_exception=True)


@pytest.mark.django_db
def test_habit_serializer_with_blank_name(habit_serializer):
    habit_serializer.initial_data['name'] = ''
    assert not habit_serializer.is_valid(raise_exception=True)
    assert habit_serializer.errors['name'][0] == 'This field may not be blank.'


@pytest.mark.django_db
def test_habit_serializer_with_invalid_is_good_habit(habit_serializer):
    habit_serializer.initial_data['is_good_habit'] = 'invalid_value'
    assert not habit_serializer.is_valid(raise_exception=True)
    assert habit_serializer.errors['is_good_habit'][0] == 'Must be a valid boolean.'
