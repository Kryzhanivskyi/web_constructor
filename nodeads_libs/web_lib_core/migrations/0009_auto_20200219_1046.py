# Generated by Django 3.0.2 on 2020-02-19 08:46

from django.db import migrations, models
import image_cropping.fields


class Migration(migrations.Migration):

    dependencies = [
        ('web_lib_core', '0008_auto_20200218_1705'),
    ]

    operations = [
        migrations.AddField(
            model_name='dimagegroup',
            name='cropping',
            field=image_cropping.fields.ImageRatioField('preview', '430x360', adapt_rotation=False, allow_fullsize=False, free_crop=False, help_text=None, hide_image_field=False, size_warning=False, verbose_name='cropping'),
        ),
        migrations.AddField(
            model_name='dimagegroup',
            name='preview_url',
            field=models.ImageField(blank=True, upload_to='content/items/upload_images'),
        ),
    ]
