from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from conversation.models import Conversation
from conversation.serializers import ConversationSerializer


@api_view(['GET'])
def get_or_create_conversation(request):
    user_name = request.query_params.get('user')
    if not user_name:
        return Response({'error': 'User name is required'}, status=status.HTTP_400_BAD_REQUEST)

    conversation, created = Conversation.objects.get_or_create(user=user_name)
    serializer = ConversationSerializer(conversation)
    return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
