# Generated by Django 3.0.2 on 2020-02-18 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_lib_core', '0007_auto_20200218_1440'),
    ]

    operations = [
        migrations.AddField(
            model_name='content',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='content',
            name='updated',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
