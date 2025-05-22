from rest_framework import serializers

class EventSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField()
    description = serializers.CharField()
    date = serializers.DateField()
    venue = serializers.CharField()
    capacity = serializers.IntegerField()
    created_at = serializers.DateTimeField(read_only=True)


class TicketSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    event_id = serializers.UUIDField()
    user_id = serializers.UUIDField()
    created_at = serializers.DateTimeField(read_only=True)

class UserSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField()
    email = serializers.EmailField()
    role = serializers.CharField()
    created_at = serializers.DateTimeField(read_only=True)
