# Generated by Django 2.2.5 on 2019-09-18 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Film',
            fields=[
                ('external_id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('date_updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-date_updated'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('external_id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('date_updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-date_updated'],
                'abstract': False,
            },
        ),
    ]
