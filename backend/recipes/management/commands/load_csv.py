import csv
import os.path as path
from django.core.management.base import BaseCommand

from recipes.models import Ingredient
from foodgram.settings import BASE_DIR

MODELS_DATA = {
    Ingredient: 'ingredients.csv',
}

FOODGRAMM_DIR = path.abspath(path.join(BASE_DIR))


class Command (BaseCommand):
    help = 'Import data from CSV file to database'

    def handle(self, *args, **options):
        for model, csv_file in MODELS_DATA.items():
            with open(
                f'{FOODGRAMM_DIR}/data/{csv_file}', mode='r',
                encoding='utf-8',
            ) as file:
                reader = csv.DictReader(file)
                inridients = []
                for row in reader:
                    inridients.append(model(**row))
            model.objects.bulk_create(inridients)
            self.stdout.write(self.style.SUCCESS(
                'Данные успешно загружены.'
            ))
