from django.contrib import admin
from .models import  Places, PlaceImage


class PlaceImageInlain(admin.TabularInline):
    model = PlaceImage
    fields = ('image', 'position')
    extra = 1


@admin.register(Places)
class PlaceAdmin(admin.ModelAdmin):
    list_display =('title', 'longitude', 'latitude')
    inlines = [PlaceImageInlain]



