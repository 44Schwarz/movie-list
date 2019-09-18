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

    def __str__(self):
        return self.name

    @staticmethod
    def retrieve_data(url_part, base_url='https://ghibliapi.herokuapp.com/'):
        url = base_url + url_part
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
    cast = models.ManyToManyField('Person')


class Person(CommonInfo):
    @classmethod
    def insert_data(cls, data):
        if not data:
            return
        for item in data:
            obj = cls(external_id=item.get('id'), name=item.get('name'))
            obj.save()
            for film_item in item.get('films'):
                film_id = cls.retrieve_data(film_item, base_url='').get('id')
                try:
                    film_obj = Film.objects.get(pk=film_id)
                except Film.DoesNotExist:  # If that film is not in our database
                    continue
                else:
                    film_obj.cast.add(obj)
                    film_obj.save()
