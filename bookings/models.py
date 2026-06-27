from django.db import models
from django.contrib.auth.models import User
from destinations.models import Destination


class Booking(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='bookings'
    )

    destination = models.ForeignKey(
        Destination,
        on_delete=models.CASCADE,
        related_name='bookings'
    )

    start_date = models.DateField(
        verbose_name='Ngày khởi hành'
    )

    people = models.PositiveIntegerField(
        default=1,
        verbose_name='Số người'
    )

    total_price = models.DecimalField(
        max_digits=12,
        decimal_places=0,
        verbose_name='Tổng tiền'
    )

    note = models.TextField(
        blank=True,
        verbose_name='Ghi chú'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f'{self.user.username} - {self.destination.name}'
