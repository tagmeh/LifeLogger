from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from django.contrib.auth import models

User = get_user_model()


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
        """ While this validation already exists at a model level. Catching it here allows for a cleaner response. """
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('An account with that email already exists.')
        return email

    def validate_passwords(self, password, repeat_password):
        if password != repeat_password:
            raise serializers.ValidationError("Passwords do not match.")

        validate_password(password=password)

    def validate(self, payload):
        self.validate_passwords(payload['password'], payload['confirm_password'])

        payload['username'] = payload['email']  # The User.create_user() method requires a username.

        return payload

    @staticmethod
    def create(validated_data: dict):
        del validated_data['confirm_password']
        return User.objects.create_user(**validated_data)



