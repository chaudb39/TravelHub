from django.db import models


class Destination(models.Model):
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    image = models.ImageField(upload_to='destinations/')
    short_description = models.TextField()
    description = models.TextField()
    price = models.IntegerField()
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
