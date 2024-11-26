from rest_framework import serializers
from .models import Text


class TextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Text
        exclude = ["recipient", "sender"]
        # fields = "__all__"

    def create(self, validated_data, recipient, sender):
        text = Text(**validated_data)
        text.sender = sender
        text.recipient = recipient
        text.save()
        return text
