from django.db import models

# Create your models here.
from shortener.models import ShortURL


class ClickEventManager(models.Manager):
    def create_event(self, shortInstance):
        if isinstance(shortInstance, ShortURL):
            obj, created = self.get_or_create(shorturl_url=shortInstance)
            obj.count += 1
            obj.save()
            return obj.count
        return None


class ClickEvent(models.Model):
    shorturl_url = models.OneToOneField(ShortURL)
    count = models.IntegerField(default=0)
    updated = models.DateTimeField(auto_now=True) # model was updated
    timestamp = models.DateTimeField(auto_now_add=True) # model was created

    objects = ClickEventManager()

    def __str__(self):
        return '{i}'.format(i=self.count)
