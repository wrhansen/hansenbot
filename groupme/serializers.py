from rest_framework import serializers


class MessageSerializer(serializers.Serializer):
    # attachments = serializers.ListField()
    avatar_url = serializers.URLField()
    created_at = serializers.IntegerField()
    group_id = serializers.CharField()
    id = serializers.CharField()
    name = serializers.CharField()
    sender_id = serializers.CharField()
    sender_type = serializers.CharField()
    source_guid = serializers.CharField()
    system = serializers.BooleanField()
    text = serializers.CharField(required=True)
    user_id = serializers.CharField()
