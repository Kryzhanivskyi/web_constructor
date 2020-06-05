# Generated by Django 3.0.2 on 2020-04-07 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_lib_core', '0042_auto_20200406_1437'),
    ]

    operations = [
        migrations.AddField(
            model_name='dimagegroup',
            name='is_visible',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AddField(
            model_name='dmusicgroup',
            name='is_visible',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AddField(
            model_name='dpostgroup',
            name='is_visible',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AddField(
            model_name='dvideogroup',
            name='is_visible',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]