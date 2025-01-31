import csv
import os.path
from functools import cached_property

from utils import CHATBOT_INPUT_DIR


class RedCrossDataHandler:
    REDCROSS_URL = 'https://helpfulinformation.redcross.nl/den-haag'

    @cached_property
    def categories(self) -> dict[int, str]:
        filename = 'categories_original.csv'
        filepath = os.path.join(CHATBOT_INPUT_DIR, filename)
        with open(filepath, 'r') as file:
            dict_reader = csv.DictReader(file)
            return {int(row['ID']): row['SLUG']
                    for row in dict_reader
                    if row['VISIBLE'].upper() == 'SHOW'}

    @cached_property
    def subcategories(self) -> dict[int, str]:
        filename = 'subcategories_original.csv'
        filepath = os.path.join(CHATBOT_INPUT_DIR, filename)
        result = {}
        with open(filepath, 'r', encoding='utf-8') as file:
            dict_reader = csv.DictReader(file)
            for row in dict_reader:
                visible = row['VISIBLE'].upper()
                if visible != 'SHOW':
                    continue
                subcategory_id = int(row['ID'])
                category_id = int(row['CATEGORY'])
                subcategory_slug = row['SLUG']
                category_slug = self.categories[category_id]
                result[subcategory_id] = f"{category_slug}/{subcategory_slug}"
        return result

    @cached_property
    def subcategory_descriptions(self) -> dict[int, str]:
        filename = 'subcategories_original.csv'
        filepath = os.path.join(CHATBOT_INPUT_DIR, filename)
        with open(filepath, 'r', encoding='utf-8') as file:
            dict_reader = csv.DictReader(file)
            return {int(row['ID']): row['DESCRIPTION'].replace('\n', ' ')
                    for row in dict_reader
                    if row['VISIBLE'].upper() == 'SHOW'}

    def get_url(self, subcategory_id: int) -> str:
        try:
            return f'{self.REDCROSS_URL}/{self.subcategories[subcategory_id]}'
        except KeyError as e:
            msg = f'Subcategory ID {subcategory_id} is not a visible subcategory.'
            raise ValueError(msg)

    def write_csv_file(self):
        input_filename = 'subcategories_original.csv'
        output_filename = 'chatbot-input.csv'
        input_filepath = os.path.join(CHATBOT_INPUT_DIR, input_filename)
        output_filepath = os.path.join(CHATBOT_INPUT_DIR, output_filename)
        result = {
            self.get_url(subcategory_id): self.subcategory_descriptions[subcategory_id]
            for subcategory_id, subcategory_slug in self.subcategories.items()
        }
        # Write the result to a new CSV file
        with open(output_filepath, 'w', newline='', encoding='utf-8') as file:
            fieldnames = ['LINK', 'DESCRIPTION']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for subcategory_slug, description in result.items():
                writer.writerow({'LINK': subcategory_slug, 'DESCRIPTION': description})



if __name__ == '__main__':
    handler = RedCrossDataHandler()
    print(handler.categories)
    print(handler.subcategories)
    print(handler.subcategory_descriptions)
    handler.write_csv_file()
    print(handler.get_url(7))
