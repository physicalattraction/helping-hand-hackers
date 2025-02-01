from django.urls import path

from conversation.views import get_or_create_conversation

urlpatterns = [
    path('', get_or_create_conversation, name='get_or_create_conversation'),
]
