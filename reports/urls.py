from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),

    path('export-csv/', views.export_booking_csv, name='export_booking_csv'),

    path(
        'booking/<int:booking_id>/pdf/',
        views.export_booking_pdf,
        name='export_booking_pdf'
    ),
]