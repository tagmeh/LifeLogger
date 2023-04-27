import pytest
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from main.serializers import UserSerializer

User = get_user_model()


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
def user(db):
    return User.objects.create_user(username='testuser', email='test@example.com', password='testpass')


@pytest.mark.django_db
def test_UserSerializer_valid_user(valid_user_data):
    serializer = UserSerializer(data=valid_user_data)
    assert serializer.is_valid()

    user = serializer.save()
    assert user.email == valid_user_data["email"]
    assert user.first_name == valid_user_data["first_name"]
    assert user.last_name == valid_user_data["last_name"]
    assert user.check_password(valid_user_data["password"])


@pytest.mark.django_db
def test_UserSerializer_invalid_email(valid_user_data):
    valid_user_data["email"] = "invalidemail"
    serializer = UserSerializer(data=valid_user_data)
    with pytest.raises(ValidationError):
        serializer.is_valid(raise_exception=True)


@pytest.mark.django_db
def test_UserSerializer_weak_password(valid_user_data):
    valid_user_data["password"] = "weak"
    valid_user_data["confirm_password"] = "weak"
    serializer = UserSerializer(data=valid_user_data)
    with pytest.raises(ValidationError):
        serializer.is_valid(raise_exception=True)


@pytest.mark.django_db
def test_UserSerializer_password_mismatch(valid_user_data):
    valid_user_data["confirm_password"] = "differentpassword"
    serializer = UserSerializer(data=valid_user_data)
    with pytest.raises(ValidationError):
        serializer.is_valid(raise_exception=True)


@pytest.mark.django_db
def test_validate_email(user):
    serializer = UserSerializer(data={'username': 'testuser2', 'email': user.email, 'password': 'testpassword'})
    with pytest.raises(ValidationError) as e:
        serializer.is_valid(raise_exception=True)

    assert 'An account with that email already exists.' in str(e.value)
