from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget

from .models import Review


class ReviewForm(forms.ModelForm):

    class Meta:

        model = Review

        fields = [
            'rating',
            'comment'
        ]

        widgets = {

            'rating': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),

            'comment': CKEditor5Widget(
                config_name='default'
            ),

        }