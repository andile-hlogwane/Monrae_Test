from rest_framework import serializers


class SentimentSerializer(serializers.Serializer):
    user_input = serializers.ListField(child=serializers.CharField())
