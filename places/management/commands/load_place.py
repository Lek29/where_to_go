import os

import requests

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand


from places.models import Place, PlaceImage


class Command(BaseCommand):
    help = 'Загружает данные о месте из JSON по URL'

    def add_arguments(self, parser):
        parser.add_argument('json_url', type=str, help='URL JSON-файла')

    def handle(self, *args, **options):
        json_url = options['json_url']
        print(f"Загружаем: {json_url}")

        try:
            response = requests.get(json_url)
            response.raise_for_status()
            raw_place = response.json()
        except Exception as e:
            print(f"Ошибка при загрузке JSON: {e}")
            return
        try:
            place_title_from_json = raw_place['title']
            coordinates = raw_place['coordinates']
            longitude_from_json = coordinates['lng']
            latitude_from_json = coordinates['lat']
        except KeyError as e:
            print(f"Ошибка: отсутствует обязательный ключ {e} в JSON по адресу {json_url}")
            return

        try:
            place_object, created = Place.objects.get_or_create(
                title=place_title_from_json,
                longitude=longitude_from_json,
                latitude=latitude_from_json,
                defaults={
                    'short_description': raw_place.get('description_short', ''),
                    'long_description': raw_place.get('description_long', ''),
                }
            )

            if created:
                print(f"Место '{place_object.title}' создано.")
            else:
                print(f"Место '{place_object.title}' найдено, добавляем/обновляем картинки.")

                place_object.images.all().delete()
        except Place.MultipleObjectsReturned:
            print('Найдены не уникальные поля')
            return

        image_urls = raw_place.get('imgs', [])
        print(f"Найдено картинок: {len(image_urls)}")

        for index, img_url in enumerate(image_urls):
            try:
                print(f"  Загрузка картинки: {img_url}")
                img_response = requests.get(img_url)
                img_response.raise_for_status()

                img_name = os.path.basename(img_url)
                img_content = ContentFile(img_response.content, name=img_name)

                PlaceImage.objects.create(
                    place=place_object,
                    image=img_content,
                    position=index
                )
                print(f"  Картинка '{img_name}' сохранена.")

            except Exception as e:
                print(f'Ошибка: {e}')
