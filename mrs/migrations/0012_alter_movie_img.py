# Generated by Django 3.2.7 on 2021-09-25 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mrs', '0011_movie_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='img',
            field=models.ImageField(blank=True, default=None, upload_to=''),
        ),
    ]
