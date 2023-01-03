from django.urls import path
from .views import register_view, login_view, user_logout, Dashboard, view_location


urlpatterns = [
    path('', register_view, name='register'),
    path('login', login_view, name='login'),
    path('logout', user_logout, name='logout'),
    path('dashboard/<str:pk>', Dashboard.as_view(), name='dashboard'),
    path('view/location/<str:pk>/<str:whose>', view_location, name='view_location'),
]
