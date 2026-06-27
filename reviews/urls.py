from django.urls import path
from . import views


app_name = 'reviews'

urlpatterns = [
    path(
        'them-danh-gia/<int:destination_id>/',
        views.add_review,
        name='add_review'
    ),
]