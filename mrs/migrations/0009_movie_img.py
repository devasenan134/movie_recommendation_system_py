# Generated by Django 3.2.7 on 2021-09-25 04:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mrs', '0008_movie_mth'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='img',
            field=models.ImageField(default=None, upload_to=''),
            preserve_default=False,
        ),
    ]
