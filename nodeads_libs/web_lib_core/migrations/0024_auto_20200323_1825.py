# Generated by Django 3.0.2 on 2020-03-23 16:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web_lib_core', '0023_posttags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dimagegrouplang',
            name='lang',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='d_image_group_langs', to='web_lib_core.Language'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='dmusicgrouplang',
            name='lang',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='d_music_group_langs', to='web_lib_core.Language'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='dpostgrouplang',
            name='lang',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='d_post_group_langs', to='web_lib_core.Language'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='dvideogrouplang',
            name='lang',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='d_video_group_langs', to='web_lib_core.Language'),
            preserve_default=False,
        ),
    ]
