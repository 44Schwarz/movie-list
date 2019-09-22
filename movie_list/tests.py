from django.test import TestCase
from django.db import IntegrityError
from django.core.exceptions import ValidationError

from .models import Person, Film


# Create your tests here.
class FilmTestCase(TestCase):
    def test_insert_data(self):
        films_list = [
            {'id': 'N1', 'title': 'Title 1', 'extra_info': 'Sth here'},
            {'id': 'N2', 'title': 'Title 2', 'extra_info': 'Sth here'},
            {'id': 'N3', 'title': 'Title 3', 'extra_info': 'Sth here'},
        ]
        Film.insert_data(films_list)
        self.assertEqual(Film.objects.count(), len(films_list))
        f2 = Film.objects.get(pk='N2')
        self.assertEqual(f2.name, 'Title 2')

    def test_insert_nothing(self):
        Film.insert_data()
        self.assertEqual(Film.objects.count(), 0)

    def test_object_representation(self):
        f = Film.objects.create(external_id='Id', name='GoodFilm')
        self.assertEqual(str(f), 'GoodFilm')

    def test_duplicate_keys(self):
        Film.objects.create(external_id='Id', name='Name')
        with self.assertRaises(IntegrityError):
            Film.objects.create(external_id='Id', name='Name')

    def test_fields_size(self):
        f = Film.objects.create(external_id='x' * 51, name='n')
        with self.assertRaises(ValidationError):
            f.full_clean()

        f = Film.objects.create(external_id='x', name='n' * 51)
        with self.assertRaises(ValidationError):
            f.full_clean()

    def test_update_field(self):
        f = Film.objects.create(external_id='N1', name='Name 1')
        Film.objects.filter(pk=f.pk).update(name='Name 2')
        f.refresh_from_db()
        self.assertEqual(f.name, 'Name 2')

    def test_time_to_update(self):
        f = Film.objects.create(external_id='N1', name='Name 1')
        self.assertFalse(f.time_to_update())

        from django.utils import timezone
        from datetime import timedelta
        Film.objects.filter(pk=f.pk).update(date_updated=timezone.now() - timedelta(minutes=1))
        f.refresh_from_db()
        self.assertTrue(f.time_to_update())


class PersonTestCase(TestCase):
    def setUp(self):
        Film.objects.create(external_id='N1', name='Title 1')
        Film.objects.create(external_id='N2', name='Title 2')
        Film.objects.create(external_id='N3', name='Title 3')

    @staticmethod
    def create_person(external_id='P1', name='Name Surname'):
        return Person.objects.create(external_id=external_id, name=name)

    def test_insert_data(self):
        people_list = [
            {'id': 'P1', 'name': 'Name 1', 'films': []},
            {'id': 'P2', 'name': 'Name 2', 'films': []},
            {'id': 'P3', 'name': 'Name 3', 'films': []},
        ]
        Person.insert_data(people_list)
        self.assertEqual(Person.objects.count(), len(people_list))

    def test_model_relations(self):
        film = Film.objects.get(pk='N3')
        self.assertEqual(film.cast.count(), 0)

        person = self.create_person()
        film.cast.add(person)
        film.save()
        self.assertEqual(film.cast.count(), 1)

        person2 = self.create_person(external_id='P2')
        film.cast.add(person2)
        film.save()
        self.assertEqual(film.cast.count(), 2)

    def test_double_cast(self):
        film = Film.objects.get(pk='N3')
        person = self.create_person()

        film.cast.add(person)
        film.save()
        self.assertEqual(film.cast.count(), 1)

        film.cast.add(person)
        film.save()
        self.assertEqual(film.cast.count(), 1)
