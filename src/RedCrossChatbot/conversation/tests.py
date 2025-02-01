from django.test import TestCase
from django.urls import reverse


class ConversationTestCase(TestCase):
    def test_url_resolves(self):
        get_or_create_url = reverse('get_or_create_conversation')
        self.assertEqual('/conversation/', get_or_create_url)
