from django.db import models
from django.contrib.auth.models import User
from django_ckeditor_5.fields import CKEditor5Field

from destinations.models import Destination


class Review(models.Model):

    destination = models.ForeignKey(
        Destination,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    rating = models.PositiveSmallIntegerField(
        choices=[
            (1, '1 sao'),
            (2, '2 sao'),
            (3, '3 sao'),
            (4, '4 sao'),
            (5, '5 sao'),
        ],
        verbose_name='Đánh giá'
    )

    comment = CKEditor5Field(
        verbose_name='Bình luận',
        config_name='default'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return (
            f'{self.user.username} - '
            f'{self.destination.name} - '
            f'{self.rating} sao'
        )