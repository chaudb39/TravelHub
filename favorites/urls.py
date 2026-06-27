from django.urls import path
from . import views

app_name = 'favorites'

urlpatterns = [
    path('', views.favorite_list, name='favorite_list'),
    path('add/<int:destination_id>/', views.add_favorite, name='add_favorite'),
    path('remove/<int:destination_id>/', views.remove_favorite, name='remove_favorite'),
    path('clear/', views.clear_favorites, name='clear_favorites'),
]