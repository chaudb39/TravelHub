from django import forms
from .models import Booking


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = [
            'start_date',
            'people',
            'note',
        ]

        widgets = {
            'start_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'people': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1
            }),
            'note': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
        }