# Generated by Django 3.0.2 on 2020-02-12 10:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web_lib_core', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='content',
            old_name='html_list',
            new_name='html',
        ),
        migrations.RenameField(
            model_name='contentlang',
            old_name='html_list',
            new_name='html',
        ),
    ]
