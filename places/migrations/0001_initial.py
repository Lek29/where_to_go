# Generated by Django 4.2.20 on 2025-05-07 13:15

import django.db.models.deletion
from django.db import migrations, models

import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название')),
                ('short_description', models.TextField(blank=True, verbose_name='Краткое описание')),
                ('long_description', tinymce.models.HTMLField(blank=True, verbose_name='Полное описание')),
                ('longitude', models.FloatField(verbose_name='Долгота')),
                ('latitude', models.FloatField(verbose_name='Широта')),
            ],
            options={
                'verbose_name': 'Интересное место',
                'verbose_name_plural': 'Интересные места',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='PlaceImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='place_images/', verbose_name='Картинка')),
                ('position', models.PositiveIntegerField(db_index=True, default=0, verbose_name='Позиция')),
                ('place', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='places.place', verbose_name='Место')),
            ],
            options={
                'verbose_name': 'Изображение места',
                'verbose_name_plural': 'Изображения места',
                'ordering': ['position'],
            },
        ),
    ]
