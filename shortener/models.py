from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class ShortenedLink(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    special_name = models.CharField(max_length=5, blank=True)
    original_link = models.URLField(blank=True)
    shortened_link = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.original_link + ' --> ' + self.shortened_link
