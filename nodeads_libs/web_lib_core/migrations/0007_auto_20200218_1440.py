# Generated by Django 3.0.2 on 2020-02-18 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_lib_core', '0006_pagelang'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dimage',
            name='preview_url',
            field=models.FileField(blank=True, upload_to='content/items/file_url'),
        ),
        migrations.AlterField(
            model_name='dimage',
            name='url',
            field=models.FileField(blank=True, upload_to='content/items/file_url'),
        ),
        migrations.AlterField(
            model_name='dmusic',
            name='preview_url',
            field=models.FileField(blank=True, upload_to='content/items/file_url'),
        ),
        migrations.AlterField(
            model_name='dmusic',
            name='url',
            field=models.FileField(blank=True, upload_to='content/items/file_url'),
        ),
        migrations.AlterField(
            model_name='dvideo',
            name='preview_url',
            field=models.FileField(blank=True, upload_to='content/items/file_url'),
        ),
        migrations.AlterField(
            model_name='dvideo',
            name='url',
            field=models.FileField(blank=True, upload_to='content/items/file_url'),
        ),
    ]
