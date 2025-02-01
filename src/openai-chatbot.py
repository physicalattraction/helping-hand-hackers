import json
import os.path
from functools import cached_property

import llm

from utils import CHATBOT_INPUT_DIR


class RedCrossChatbot:
    @cached_property
    def secrets(self) -> dict[str, object]:
        with open('secrets.json') as f:
            return json.load(f)

    @cached_property
    def chatbot_input(self) -> str:
        chatbot_input_filename = 'chatbot-input.csv'
        chatbot_input_filepath = os.path.join(CHATBOT_INPUT_DIR, chatbot_input_filename)
        with open(chatbot_input_filepath) as f:
            return f.read()

    @cached_property
    def initial_prompt(self):
        return (f'You are a chatbot, a helpful assistant to refugees. '
                f'You have the following csv to you available. It contains links, and the descriptions on what to '
                f'find at that link. Use this csv as your knowledge base. {self.chatbot_input}. '
                f'You ')

    def run(self):
        model = llm.get_model('gpt-4o-mini')
        model.key = self.secrets['OPENAI_KEY']
        initial_prompt_initialized = False
        conversation = model.conversation()
        while True:
            user_input = input('You: ')
            if user_input.lower() in {'exit', 'bye', 'quit'}:
                break
            if not initial_prompt_initialized:
                user_input = self.initial_prompt + user_input
                initial_prompt_initialized = True
            response = conversation.prompt(user_input)
            print(response.text())


if __name__ == '__main__':
    chatbot = RedCrossChatbot()
    chatbot.run()
