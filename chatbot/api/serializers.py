from rest_framework import serializers

class CHAT_MESSAGE_SERIALIZER(serializers.Serializer):
    message = serializers.CharField()
