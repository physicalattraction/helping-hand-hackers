import csv
import os.path
from functools import cached_property
import json

from utils import CHATBOT_INPUT_DIR


class RedCrossDataHandler:
    REDCROSS_URL = 'https://helpfulinformation.redcross.nl/den-haag'

    @cached_property
    def categories(self) -> dict[int, str]:
        """
        Return a dictionary from category ID to category slug
        """

        filename = 'categories_original.csv'
        filepath = os.path.join(CHATBOT_INPUT_DIR, filename)
        with open(filepath, 'r') as file:
            dict_reader = csv.DictReader(file)
            return {int(row['ID']): row['SLUG']
                    for row in dict_reader
                    if row['VISIBLE'].upper() == 'SHOW'}

    @cached_property
    def subcategories(self) -> dict[int, str]:
        """
        Return a dictionary from subcategory ID to <category_slug>/<subcategory_slug>
        """

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
        """
        Return a dictionary from subcategory ID to subcategory description
        """

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
            raise ValueError(msg) from e

    def write_csv_file(self):
        output_filename = 'chatbot-input.csv'
        output_filepath = os.path.join(CHATBOT_INPUT_DIR, output_filename)
        result = {
            self.get_url(subcategory_id): self.subcategory_descriptions[subcategory_id]
            for subcategory_id, subcategory_slug in self.subcategories.items()
        }

        offers_filename = "Offers.csv"
        offers_filepath = os.path.join(CHATBOT_INPUT_DIR, offers_filename)
        with open(offers_filepath, 'r', encoding='utf-8') as file:
            dict_reader = csv.DictReader(file)
            for row in dict_reader:
                visible = row['VISIBLE'].upper()
                if visible != 'SHOW':
                    print('This line is hidden')
                    continue
                
                try:
                    subcategory_id = int(row['SUBCATEGORY'])
                except ValueError:
                    continue
                try:
                    subcategory_link = self.get_url(subcategory_id)
                except ValueError:
                    continue
                offer_slug = row['SLUG']
                link = f'{subcategory_link}/{offer_slug}'
                print(link)

                description = f'{row["NAME"]}: {row["DESCRIPTION"].replace("\n", " ")}. Phone: {row["PHONENUMBERS"].replace("\n", ", ") or "unknown"}. Email: {row["EMAILS"] or "unknown"}.'
                result[link] = description


        # Write the result to a new CSV file
        with open(output_filepath, 'w', newline='', encoding='utf-8') as file:
            fieldnames = ['LINK', 'DESCRIPTION']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for subcategory_slug, description in result.items():
                writer.writerow({'LINK': subcategory_slug, 'DESCRIPTION': description})

if __name__ == '__main__':
    handler = RedCrossDataHandler()
    # print(handler.categories)
    # print(handler.subcategories)
    # print(handler.subcategory_descriptions)
    handler.write_csv_file()
    print(handler.get_url(7))