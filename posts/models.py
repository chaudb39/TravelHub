from django.db import models
from django_ckeditor_5.fields import CKEditor5Field


class Post(models.Model):
    title = models.CharField(max_length=200)
    thumbnail = models.ImageField(upload_to='posts/')
    summary = models.TextField()
    content = CKEditor5Field('Nội dung bài viết', config_name='default')
    author = models.CharField(max_length=100, default='TravelHub')
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title