from django.contrib import admin

from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin

from .models import Place, PlaceImage


class PlaceImageInline(SortableInlineAdminMixin,
                      admin.TabularInline):
    model = PlaceImage
    fields = ('image', 'get_preview_html')
    readonly_fields = ('get_preview_html',)
    extra = 1


@admin.register(Place)
class PlaceAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('title', 'longitude', 'latitude')
    search_fields = ['title', 'short_description']
    inlines = [PlaceImageInline]


@admin.register(PlaceImage)
class PlaceImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'place', 'position', 'get_preview_html')
    autocomplete_fields = ['place']


    readonly_fields = ('get_preview_html',)


