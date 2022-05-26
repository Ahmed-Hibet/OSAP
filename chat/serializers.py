from rest_framework import serializers
from .models import Message
from access.serializers import UserCreateSerializer


class MessageSerializer(serializers.ModelSerializer):
    sender = UserCreateSerializer(required=False, allow_null=True)
    receiver = UserCreateSerializer(required=False, allow_null=True)
    class Meta:
        model = Message
        fields = ['id', 'sender', 'receiver', 'message', 'created_at']