from django.urls import path
from . import views


urlpatterns = [
    path('add/location', views.add_location, name='add_location'),
    path('update/location', views.update_location, name='update_location'),
    path('delete/location/<str:pk>', views.delete_location, name='delete_location'),
    path('', views.view_map, name='map'),
    path('get/direction', views.get_direction, name='get_direction'),
]
