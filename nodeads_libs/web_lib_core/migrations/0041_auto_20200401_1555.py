# Generated by Django 3.0.2 on 2020-04-01 12:55

from django.db import migrations
import image_cropping.fields


class Migration(migrations.Migration):

    dependencies = [
        ('web_lib_core', '0040_auto_20200401_1231'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dpostimage',
            name='cropping',
            field=image_cropping.fields.ImageRatioField('image', '600x300', adapt_rotation=False, allow_fullsize=False, free_crop=False, help_text=None, hide_image_field=False, size_warning=True, verbose_name='cropping'),
        ),
    ]
