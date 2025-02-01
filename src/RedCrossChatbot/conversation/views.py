from rest_framework import status, viewsets
from rest_framework.response import Response

from chatbot.chatbot import Chatbot
from conversation.models import Conversation
from conversation.serializers import ConversationSerializer


class ConversationViewSet(viewsets.ViewSet):
    def list(self, request):
        user_name = request.query_params.get('user')
        if not user_name:
            return Response({'error': 'User name is required'}, status=status.HTTP_400_BAD_REQUEST)

        conversation, created = Conversation.objects.get_or_create(user=user_name)
        serializer = ConversationSerializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

    def create(self, request):
        print(request.data)
        user_name = request.data.get('user')
        text = request.data.get('text')
        if not user_name:
            return Response({'error': 'User name is required'}, status=status.HTTP_400_BAD_REQUEST)
        if not text:
            return Response({'error': 'Text is required'}, status=status.HTTP_400_BAD_REQUEST)

        conversation, _ = Conversation.objects.get_or_create(user=user_name)
        conversation.lines.create(speaker='user', text=text)

        chatbot = Chatbot(user_name)
        result = chatbot.respond_to(text)

        conversation.lines.create(speaker='bot', text=result)
        return Response(status=status.HTTP_201_CREATED, data={'response': result})
