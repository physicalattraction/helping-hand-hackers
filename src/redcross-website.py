import csv
import os.path
from functools import cached_property

from utils import CHATBOT_INPUT_DIR


class RedCrossDataHandler:
    REDCROSS_URL = 'https://helpfulinformation.redcross.nl/den-haag'

    @cached_property
    def categories(self) -> dict[int, str]:
        filename = 'categories.csv'
        filepath = os.path.join(CHATBOT_INPUT_DIR, filename)
        with open(filepath, 'r') as file:
            dict_reader = csv.DictReader(file)
            return {int(row['ID']): row['SLUG'] for row in dict_reader if row['SLUG']}

    @cached_property
    def subcategories(self) -> dict[int, str]:
        filename = 'subcategories.csv'
        filepath = os.path.join(CHATBOT_INPUT_DIR, filename)
        result = {}
        with open(filepath, 'r') as file:
            dict_reader = csv.DictReader(file)
            for row in dict_reader:
                visible = row['VISIBLE']
                subcategory_id = int(row['ID'])
                category_id = int(row['CATEGORY'])
                subcategory_slug = row['SLUG']
                category_slug = self.categories[category_id]
                result[subcategory_id] = f"{category_slug}/{subcategory_slug}"
        return result

    def get_url(self, subcategory_id: int) -> str:
        return f'{self.REDCROSS_URL}/{self.subcategories[subcategory_id]}'


if __name__ == '__main__':
    handler = RedCrossDataHandler()
    # print(handler.categories)
    # print(handler.subcategories)
    print(handler.get_url(8))
