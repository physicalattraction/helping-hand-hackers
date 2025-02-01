from rest_framework import serializers

from conversation.models import ConversationLine, Conversation


class ConversationLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConversationLine
        fields = '__all__'


class ConversationSerializer(serializers.ModelSerializer):
    lines = ConversationLineSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['id', 'user', 'created_at', 'updated_at', 'lines']
