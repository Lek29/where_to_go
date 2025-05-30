from django.db import models
from django.utils.html import format_html

from tinymce.models import HTMLField


class Place(models.Model):
    title = models.CharField(
        'Название',
        max_length=200
    )
    short_description = models.TextField(
        'Краткое описание',
        blank=True
    )
    long_description = HTMLField(
        'Полное описание',
        blank=True
    )
    longitude = models.FloatField(
        'Долгота',
    )
    latitude = models.FloatField(
        'Широта'
    )

    class Meta:
        ordering = ['title']
        verbose_name = 'Интересное место'
        verbose_name_plural = 'Интересные места'
        unique_together = [['title', 'longitude', 'latitude']]

    def __str__(self):
        return self.title


class PlaceImage(models.Model):
    place = models.ForeignKey(
        Place,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Место'
    )
    image = models.ImageField(
        'Картинка',
        upload_to='place_images/'
    )
    position = models.PositiveIntegerField(
            'Позиция',
            default=0,
            db_index=True
    )

    class Meta:
        ordering = ['position']
        verbose_name = 'Изображение места'
        verbose_name_plural = 'Изображения места'

    def __str__(self):
        try:
            return f'{self.position} {self.place.title}'
        except (Place.DoesNotExist, AttributeError):
            return f'{self.position} (Место не указано или еще не сохранено)'

    def get_preview_html(self):
        if self.image and hasattr(self.image, 'url'):
            return format_html(
                '<img src="{url}" style="max-height: 200px; max-width: 200px;" />',
                url=self.image.url
            )
        return 'Нет изображения или объект не сохранен'

    get_preview_html.short_description = 'Предпросмотр'
