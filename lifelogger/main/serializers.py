from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth import models

User = get_user_model()


class UserSerializer(serializers.ModelSerializer[models.User]):
    password = serializers.CharField(write_only=True)
    repeat_password = serializers.CharField(write_only=True)
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'username', 'password', 'repeat_password']
        read_only_fields = ('username',)

    @staticmethod
    def validate_username(username):
        """ While this validation already exists at a model level. Catching it here allows for a cleaner response. """
        if User.objects.get(username=username):
            raise serializers.ValidationError('An account with that username already exists.')
        return username

    def validate(self, payload):
        self.validate_passwords(payload['password'], payload['repeat_password'])

        email = payload['email']
        if email:
            payload['username'] = email

        self.validate_username(username=payload['username'])

        return payload

    def validate_passwords(self, password, repeat_password):
        if password != repeat_password:
            raise serializers.ValidationError("Passwords do not match.")

    def create(self, validated_data: dict):
        del validated_data['repeat_password']
        return super().create(validated_data=validated_data)


