# Generated by Django 3.2.7 on 2021-09-25 04:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mrs', '0009_movie_img'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='img',
        ),
    ]