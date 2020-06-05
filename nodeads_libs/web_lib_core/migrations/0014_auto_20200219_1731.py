# Generated by Django 3.0.2 on 2020-02-19 15:31

from django.db import migrations, models
import nodeads_libs.web_lib_core.models
import nodeads_libs.web_lib_core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('web_lib_core', '0013_auto_20200219_1123'),
    ]

    operations = [
        migrations.AddField(
            model_name='dimagegroup',
            name='order_index',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='dmusicgroup',
            name='order_index',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='dvideogroup',
            name='order_index',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='dimage',
            name='order_index',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='dimage',
            name='preview_url',
            field=models.FileField(blank=True, upload_to=nodeads_libs.web_lib_core.models.type_based_upload_to, validators=[nodeads_libs.web_lib_core.validators.validate_size]),
        ),
        migrations.AlterField(
            model_name='dimage',
            name='url',
            field=models.FileField(blank=True, upload_to=nodeads_libs.web_lib_core.models.type_based_upload_to, validators=[nodeads_libs.web_lib_core.validators.validate_size]),
        ),
        migrations.AlterField(
            model_name='dimagegroup',
            name='preview_url',
            field=models.ImageField(blank=True, null=True, upload_to='content/items/group_prev/images', validators=[nodeads_libs.web_lib_core.validators.validate_size]),
        ),
        migrations.AlterField(
            model_name='dmusic',
            name='order_index',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='dmusic',
            name='preview_url',
            field=models.FileField(blank=True, upload_to=nodeads_libs.web_lib_core.models.type_based_upload_to, validators=[nodeads_libs.web_lib_core.validators.validate_size]),
        ),
        migrations.AlterField(
            model_name='dmusic',
            name='url',
            field=models.FileField(blank=True, upload_to=nodeads_libs.web_lib_core.models.type_based_upload_to, validators=[nodeads_libs.web_lib_core.validators.validate_size]),
        ),
        migrations.AlterField(
            model_name='dvideo',
            name='order_index',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='dvideo',
            name='preview_url',
            field=models.FileField(blank=True, upload_to=nodeads_libs.web_lib_core.models.type_based_upload_to, validators=[nodeads_libs.web_lib_core.validators.validate_size]),
        ),
        migrations.AlterField(
            model_name='dvideo',
            name='url',
            field=models.FileField(blank=True, upload_to=nodeads_libs.web_lib_core.models.type_based_upload_to, validators=[nodeads_libs.web_lib_core.validators.validate_size]),
        ),
    ]