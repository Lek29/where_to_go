from django.urls import path
from . import views


app_name = 'places'

urlpatterns = [
    path('', views.show_index_page, name='index'),
    path('places/<int:place_id>/', views.place_detail_api_view, name='place_detail_api')
]
