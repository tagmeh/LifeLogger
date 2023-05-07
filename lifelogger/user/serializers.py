import logging

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from django.contrib.auth import models

User = get_user_model()
log = logging.getLogger(__name__)


def validate_passwords(password, confirm_password):
    """
    Run through a few checks to validate the new passwords.
    Check 1: Validate both passwords exist
    Check 2: Validate both passwords match
    Check 3: Using Django's built in validate_password, validate the passwords aren't too common or too short.
    """
    if all([password, confirm_password]):
        if password != confirm_password:
            raise serializers.ValidationError("New passwords are not the same.")

        # No sense in validating the password if the confirm_password wasn't passed in, or doesn't match the password.
        validate_password(password=password)  # Validate password is long and strong enough. Raises errors on its own.

    else:
        # This shouldn't be trigger-able unless there's a coding issue.
        # The built-in CharField validators should require something to be passed in, which then gets validated above.
        raise serializers.ValidationError('Missing one or both new passwords.')


class PasswordUpdateSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    def validate_old_password(self, old_password):
        """Validate that the old_password matches the existing password."""
        log.debug('validating old_password')

        if self.context['request'].user.check_password(raw_password=old_password) is False:
            raise serializers.ValidationError("Old password does not match the existing password.")

        return old_password

    def validate_new_password(self, new_password):
        """Validate the new password is not the same as the existing/old password."""
        if check_password(password=new_password, encoded=self.context['request'].user.password) is True:
            # This error shouldn't expose any new information, as only logged-in users can change their password.
            # And they can only change their own password.
            raise serializers.ValidationError("New password cannot be the same as the old password.")

        return new_password

    def validate(self, payload):
        """
        At this point, simply call a shared validate_passwords
        function in order to do a few more checks on the password.
        """
        validate_passwords(payload.get('new_password'), payload.get('confirm_password'))

        return payload


class UserSerializer(serializers.ModelSerializer[models.User]):
    password = serializers.CharField(required=True, write_only=True)
    confirm_password = serializers.CharField(required=True, write_only=True)
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'password', 'confirm_password']

    @staticmethod
    def validate_email(email):
        """While this validation already exists at a model level. Catching it here allows for a cleaner response."""
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('An user with that email already exists.')
        return email

    def validate(self, payload):
        """ """
        validate_passwords(payload.get('password'), payload.get('confirm_password'))

        if payload.get('email'):
            payload['username'] = payload['email']  # The User.create_user() method requires a username.

        return payload

    def create(self, validated_data: dict):
        """
        Simple create method. Must remove confirm_password, as that's not part of the User model.
        """
        del validated_data['confirm_password']
        return User.objects.create_user(**validated_data)

    def update(self, instance: User, validated_data: dict):
        """
        Partial update that may or may not have to handle M2M fields, so the super() is called to handle those.
        """
        for field, value in validated_data.items():
            instance.field = value

        return super().update(instance, validated_data)
