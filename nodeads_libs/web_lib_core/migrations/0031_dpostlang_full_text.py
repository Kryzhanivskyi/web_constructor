# Generated by Django 3.0.2 on 2020-03-24 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_lib_core', '0030_merge_20200324_1002'),
    ]

    operations = [
        migrations.AddField(
            model_name='dpostlang',
            name='full_text',
            field=models.TextField(default='text_to_fill'),
            preserve_default=False,
        ),
    ]
