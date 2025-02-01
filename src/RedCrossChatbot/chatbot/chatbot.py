import json
import os.path
from functools import cached_property

import llm
from django.conf import settings

from conversation.models import Conversation

SRC_DIR = settings.BASE_DIR.parent
ROOT_DIR = SRC_DIR.parent
DATA_DIR = ROOT_DIR / 'data'
CHATBOT_INPUT_DIR = DATA_DIR / 'chatbot-input'


class Chatbot:
    def __init__(self, user: str):
        try:
            self.conversation = Conversation.objects.filter(user=user).prefetch_related('lines').get()
        except Conversation.DoesNotExist:
            self.conversation = Conversation.objects.create(user=user)
        self.model = llm.get_model('gpt-4o-mini')
        self.model.key = self.secrets['OPENAI_KEY']
        self.initial_prompt_initialized = False
        self.openai_conversation = self.model.conversation()

    @cached_property
    def secrets(self) -> dict[str, object]:
        with open(settings.BASE_DIR.parent / 'secrets.json') as f:
            return json.load(f)

    @cached_property
    def chatbot_input(self) -> str:
        chatbot_input_filename = 'chatbot-input.csv'
        print(CHATBOT_INPUT_DIR)
        chatbot_input_filepath = os.path.join(CHATBOT_INPUT_DIR, chatbot_input_filename)
        with open(chatbot_input_filepath) as f:
            return f.read()

    @cached_property
    def initial_prompt(self):
        return (f'You are a chatbot, a helpful assistant to refugees. '
                f'You have the following csv to you available. It contains links, and the descriptions on what to '
                f'find at that link. Use this csv as your knowledge base. {self.chatbot_input}. '
                f'')

    def respond_to(self, user_input: str) -> str:
        if user_input.lower() in {'exit', 'bye', 'quit'}:
            return 'Goodbye!'
        if not self.initial_prompt_initialized:
            user_input = self.initial_prompt + user_input
            self.initial_prompt_initialized = True
        response = self.openai_conversation.prompt(user_input)
        return response.text()
