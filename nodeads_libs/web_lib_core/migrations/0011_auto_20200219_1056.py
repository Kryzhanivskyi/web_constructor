# Generated by Django 3.0.2 on 2020-02-19 08:56

from django.db import migrations
import image_cropping.fields


class Migration(migrations.Migration):

    dependencies = [
        ('web_lib_core', '0010_auto_20200219_1049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dimagegroup',
            name='cropping',
            field=image_cropping.fields.ImageRatioField('preview_url', '150x150', adapt_rotation=False, allow_fullsize=False, free_crop=False, help_text=None, hide_image_field=False, size_warning=True, verbose_name='cropping'),
        ),
    ]
