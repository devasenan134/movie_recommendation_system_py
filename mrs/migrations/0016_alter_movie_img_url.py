# Generated by Django 3.2.7 on 2021-09-25 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mrs', '0015_alter_movie_img_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='img_url',
            field=models.URLField(blank=True),
        ),
    ]
