# Generated by Django 3.0.2 on 2020-04-06 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_lib_core', '0041_auto_20200401_1555'),
    ]

    operations = [
        migrations.AddField(
            model_name='dpost',
            name='view_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='dpostlang',
            name='view_count',
            field=models.IntegerField(default=0),
        ),
    ]
