from rest_framework import serializers
from .models import VitalLog


class VitalLogSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = VitalLog
        fields = ['id', 'vital_type', 'value', 'created_at', 'user']
        read_only_fields = ['created_at', 'user']
