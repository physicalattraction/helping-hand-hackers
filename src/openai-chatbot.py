import csv
import json
import os.path
from functools import cached_property

import llm
import requests
import tiktoken
from llm import Conversation

from utils import CHATBOT_INPUT_DIR, SRC_DIR


class RedCrossChatbot:
    MODEL = 'gpt-4o-mini'

    @cached_property
    def secrets(self) -> dict[str, object]:
        path_to_secrets = SRC_DIR / 'secrets.json'
        with open(path_to_secrets) as f:
            return json.load(f)

    @cached_property
    def chatbot_input(self) -> dict[str, str]:
        chatbot_input_filename = 'chatbot-input.csv'
        chatbot_input_filepath = os.path.join(CHATBOT_INPUT_DIR, chatbot_input_filename)
        with open(chatbot_input_filepath) as f:
            reader = csv.DictReader(f)
            return {
                row['LINK'].replace('https://helpfulinformation.redcross.nl/den-haag/', ''):
                    row['DESCRIPTION'] for row in reader
            }

    @cached_property
    def categories(self) -> list[str]:
        categories = set()
        for row in self.chatbot_input.keys():
            category_and_sub = row.replace('https://helpfulinformation.redcross.nl/den-haag/', '').split('/')[:2]
            categories.add('/'.join(category_and_sub))
        return sorted(categories)

    @cached_property
    def conversation(self) -> Conversation:
        model = llm.get_model(self.MODEL)
        model.key = self.secrets['OPENAI_KEY']
        return model.conversation()

    def find_most_fitting_category(self, user_input: str) -> str:
        prompt_str = (f'Respond with a JSON list with three strings, without formatting. '
                      f'Each string should be a category only from the following list: {self.categories}. '
                      f'Pick the three that most likely contains information about the following prompt: '
                      f'"{user_input}"')
        return self.prompt(prompt_str)

    def knowledge_based_prompt(self, categories: list[str], user_input: str) -> str:
        knowledge_lines = []
        for link, description in self.chatbot_input.items():
            if any(cat in link for cat in categories):
                knowledge_lines.append(f'{link},{description}')
        knowledge = '\n'.join(knowledge_lines)

        prompt_str = ('You are a chatbot, a helpful assistant to refugees. You have the following csv to you '
                      'available. It contains links, and the descriptions on what to find at that link. '
                      f'Use this csv as your knowledge base.\n{knowledge}.\n'
                      f'Provide a response to the following prompt. '
                      f'When referring to a page, provide the link. "{user_input}"')
        return self.prompt(prompt_str)

    def run(self):
        while True:
            user_input = input('You: ')
            if user_input.lower() in {'exit', 'bye', 'quit'}:
                break
            most_likely_categories_str = self.find_most_fitting_category(user_input)
            most_likely_categories = json.loads(most_likely_categories_str)
            print(most_likely_categories)
            self.knowledge_based_prompt(most_likely_categories, user_input)

    def prompt(self, prompt_str: str) -> str:
        self.count_tokens(prompt_str)
        # response = self.conversation.prompt(prompt_str, max_tokens=100)
        key = self.secrets['GEMINI_KEY']
        gemini_url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={key}'
        data = {
            'contents': [{
                'parts': [{'text': prompt_str}]
            }]
        }
        response = requests.post(gemini_url, json=data)
        response_json = response.json()
        usageMetadata = response_json['usageMetadata']
        print(f'{usageMetadata["promptTokenCount"]=}, '
              f'{usageMetadata["candidatesTokenCount"]=}, '
              f'{usageMetadata["totalTokenCount"]=}')
        return response_json['candidates'][0]['content']['parts'][0]['text']

    def count_tokens(self, text: str) -> int:
        encoding = tiktoken.encoding_for_model(self.MODEL)
        num_tokens = len(encoding.encode(text))
        # print('Number of input tokens: ', num_tokens)
        if num_tokens > 10_000:
            raise NotImplementedError(f'Input too long ({num_tokens}). Please try again.')
        return num_tokens


if __name__ == '__main__':
    chatbot = RedCrossChatbot()
    print(chatbot.count_tokens('Where can I sleep tonight?'))
    # print(chatbot.find_most_fitting_category('Where can I sleep tonight?'))
    # print(chatbot.knowledge_based_prompt(
    #     ['shelter/day-shelter', 'shelter/night-shelter', 'safety-protection/safety-protection'],
    #     'Where can I sleep tonight?')
    # )
    # chatbot.run()
