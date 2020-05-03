from django.db import models

# Create your models here.
from django.utils import timezone


class Category(models.Model):
    name = models.CharField('Title', max_length=255)

    def __str__(self):
        return self.name

class DiaryQuerySet(models.QuerySet):

    def published(self):
        return self.filter(created_at__lte=timezone.now())

class Diary(models.Model):
    title = models.CharField('Title', max_length=32)
    text = models.TextField('Contents')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='Category')
    created_at = models.DateTimeField('Date', default=timezone.now)
    objects = DiaryQuerySet.as_manager()

    def __str__(self):
        return self.title
