# Generated by Django 3.0.2 on 2020-03-23 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_lib_core', '0028_auto_20200323_2154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dimagelang',
            name='name',
            field=models.CharField(max_length=1024),
        ),
        migrations.AlterField(
            model_name='dmusiclang',
            name='name',
            field=models.CharField(max_length=1024),
        ),
        migrations.AlterField(
            model_name='dpostlang',
            name='name',
            field=models.CharField(max_length=1024),
        ),
        migrations.AlterField(
            model_name='dposttaglang',
            name='name',
            field=models.CharField(max_length=1024),
        ),
        migrations.AlterField(
            model_name='dvideolang',
            name='name',
            field=models.CharField(max_length=1024),
        ),
    ]
