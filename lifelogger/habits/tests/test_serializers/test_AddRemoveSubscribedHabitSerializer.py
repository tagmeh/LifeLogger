import pytest

from habits.serializers import AddRemoveSubscribedHabitSerializer


@pytest.mark.django_db
def test_add_remove_subscribed_habit_serializer_validate_habit_ids():
    unique_payload = {"habit_ids": [1, 2, 3, 4, 5, 6, 7, 8, 9]}
    duplicates_payload = {"habit_ids": [1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4]}

    serializer = AddRemoveSubscribedHabitSerializer(data=unique_payload)
    serializer.is_valid(raise_exception=True)
    assert len(serializer.validated_data['habit_ids']) == 9

    serializer = AddRemoveSubscribedHabitSerializer(data=duplicates_payload)
    serializer.is_valid(raise_exception=True)
    assert len(serializer.validated_data['habit_ids']) == 4