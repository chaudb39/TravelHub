from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='Số điện thoại'
    )

    address = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Địa chỉ'
    )

    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        verbose_name='Ảnh đại diện'
    )

    bio = models.TextField(
        blank=True,
        verbose_name='Giới thiệu'
    )

    def __str__(self):
        return self.user.username