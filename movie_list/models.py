import json
from datetime import timedelta

import requests
from django.db import models
from django.utils import timezone


# Create your models here.
class CommonInfo(models.Model):
    external_id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=50)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-date_updated']

    def __str__(self):
        return self.name

    @staticmethod
    def retrieve_data(url_part):
        url = 'https://ghibliapi.herokuapp.com/{}/'.format(url_part)
        resp = requests.get(url)
        if resp.status_code != 200:
            return None
        return json.loads(resp.text)

    @classmethod
    def insert_data(cls, data):
        if not data:
            return
        for item in data:
            obj = cls(external_id=item.get('id'), name=item.get('title'))
            obj.save()

    def time_to_update(self):
        return timezone.now() > self.date_updated + timedelta(minutes=1)


class Film(CommonInfo):
    pass
    # cast = models.ManyToManyField('Person')


class Person(CommonInfo):
    pass
