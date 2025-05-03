from django.db import models
from django.utils.html import format_html
from django.utils.text import slugify
from pytils import translit
from tinymce.models import HTMLField


class Places(models.Model):
    title = models.CharField(
        'Название',
        max_length=200
    )
    place_id_slug = models.SlugField(
        "Идентификатор для URL (слаг)",
        max_length=100,
        unique=True,
        blank=True,
        db_index=True
    )
    description_short = models.TextField(
        'Краткое описание',
        blank=True
    )
    description_long = HTMLField(
        'Полное описание',
        blank=True
    )
    longitude = models.FloatField(
        'Долгота'
    )
    latitude = models.FloatField(
        'Широта'
    )


    def __str__(self):
        return self.title


    def save(self, *args, **kwargs):
        if not self.place_id_slug:
            title_processed = self.title
            title_processed = title_processed.replace('«', '"').replace('»', '"')
            title_processed = title_processed.replace('„', '"').replace('“', '"')
            title_processed = title_processed.replace('°', '')
            title_processed = title_processed.replace('\u00A0', ' ')
            latin_title = translit.translify(title_processed)
            self.place_id_slug = slugify(latin_title)

        super().save(*args, **kwargs)


    class Meta:
        ordering = ['title']
        verbose_name = 'Интересное место'
        verbose_name_plural = 'Интересные места'


class PlaceImage(models.Model):
    place = models.ForeignKey(
        Places,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Место'
    )
    image = models.ImageField(
        'Картинка',
        upload_to='place_images/'
    )
    position=models.PositiveIntegerField(
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
        except (Places.DoesNotExist, AttributeError):
            return f"{self.position} (Место не указано или еще не сохранено)"


    def get_preview_html(self):
        if self.image and hasattr(self.image, 'url'):
            return format_html(
                '<img src="{url}" style="max-height: 200px; width: auto;" />',
                url=self.image.url
            )
        return "Нет изображения или объект не сохранен"


    get_preview_html.short_description = 'Предпросмотр'

