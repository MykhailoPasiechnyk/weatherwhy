from django.contrib.auth.models import User
from django.db import models


class City(models.Model):
    title = models.CharField(max_length=250, verbose_name='City name')
    users = models.ManyToManyField(User)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title
