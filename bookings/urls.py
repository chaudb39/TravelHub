from django.urls import path
from . import views


app_name = 'bookings'

urlpatterns = [

    path(
        'dat-chuyen/<int:destination_id>/',
        views.create_booking,
        name='create_booking'
    ),

    path(
        'lich-su/',
        views.booking_history,
        name='booking_history'
    ),

]