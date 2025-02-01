from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse

from chatbot.chatbot import Chatbot
from conversation.models import Conversation


class ConversationTestCase(TestCase):
    def test_url_resolves(self):
        get_or_create_url = reverse('conversation-list')
        self.assertEqual('/conversation/', get_or_create_url)

    def test_create_line(self):
        create_url = reverse('conversation-list')
        data = {
            'user': 'Erwin',
            'text': 'Where can I sleep tonight?'
        }
        with patch.object(Chatbot, 'respond_to', return_value='In the shelter.') as mock_respond_to:
            response = self.client.post(create_url, data=data)

        self.assertEqual(201, response.status_code)
        self.assertEqual('In the shelter.', response.data['response'])

        convo = Conversation.objects.get(user='Erwin')
        self.assertEqual(2, convo.lines.count())
        first_line = convo.lines.first()
        self.assertEqual('user', first_line.speaker)
        self.assertEqual('Where can I sleep tonight?', first_line.text)
        second_line = convo.lines.last()
        self.assertEqual('bot', second_line.speaker)
        self.assertEqual('In the shelter.', second_line.text)
