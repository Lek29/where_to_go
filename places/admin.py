from django.contrib import admin
from .models import  Places, PlaceImage


class PlaceImageInlin(admin.TabularInline):
    model = PlaceImage
    fields = ('image', 'get_preview_html', 'position')
    readonly_fields = ('get_preview_html',)
    extra = 1


@admin.register(Places)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ('title', 'longitude', 'latitude')
    search_fields = ['title', 'description_short']
    inlines = [PlaceImageInlin]



