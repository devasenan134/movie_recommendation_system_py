# Generated by Django 3.2.7 on 2021-09-28 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mrs', '0023_alter_movie_avg_rate'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='movie_url',
            field=models.URLField(blank=True),
        ),
    ]
