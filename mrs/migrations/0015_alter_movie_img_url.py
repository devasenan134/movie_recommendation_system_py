# Generated by Django 3.2.7 on 2021-09-25 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mrs', '0014_alter_movie_img_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='img_url',
            field=models.URLField(default='https://google.com'),
        ),
    ]
