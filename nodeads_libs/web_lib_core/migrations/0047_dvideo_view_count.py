# Generated by Django 3.0.2 on 2020-04-08 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_lib_core', '0046_dvideotaglang'),
    ]

    operations = [
        migrations.AddField(
            model_name='dvideo',
            name='view_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
