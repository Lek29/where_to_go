from django.contrib import admin
from .models import  Places, PlaceImage
from adminsortable2.admin import SortableInlineAdminMixin, SortableAdminMixin


class PlaceImageInline(SortableInlineAdminMixin,
                      admin.TabularInline):
    model = PlaceImage
    fields = ('image', 'get_preview_html')
    readonly_fields = ('get_preview_html',)
    extra = 1


@admin.register(Places)
class PlaceAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('title', 'longitude', 'latitude')
    search_fields = ['title', 'description_short']
    inlines = [PlaceImageInline]



