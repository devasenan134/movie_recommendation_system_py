# Generated by Django 3.2.7 on 2021-09-24 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mrs', '0002_auto_20210924_1635'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='year',
            field=models.PositiveIntegerField(default=None),
        ),
    ]
