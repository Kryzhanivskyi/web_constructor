# Generated by Django 3.0.2 on 2020-02-13 15:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web_lib_core', '0004_auto_20200213_1306'),
    ]

    operations = [
        migrations.CreateModel(
            name='DImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(blank=True, max_length=250)),
                ('preview_url', models.CharField(blank=True, max_length=250)),
                ('is_visible', models.BooleanField(blank=True, default=False)),
                ('order_index', models.PositiveSmallIntegerField()),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'db_table': 'd_image',
                'default_related_name': 'd_images',
            },
        ),
        migrations.CreateModel(
            name='DImageGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
            ],
            options={
                'db_table': 'd_image_group',
                'default_related_name': 'd_image_groups',
            },
        ),
        migrations.CreateModel(
            name='DMusic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(blank=True, max_length=250)),
                ('preview_url', models.CharField(blank=True, max_length=250)),
                ('is_visible', models.BooleanField(blank=True, default=False)),
                ('order_index', models.PositiveSmallIntegerField()),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('minus_url', models.CharField(blank=True, max_length=250)),
                ('video_url', models.CharField(blank=True, max_length=250)),
            ],
            options={
                'db_table': 'd_music',
                'default_related_name': 'd_musics',
            },
        ),
        migrations.CreateModel(
            name='DMusicGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
            ],
            options={
                'db_table': 'd_music_group',
                'default_related_name': 'd_music_groups',
            },
        ),
        migrations.CreateModel(
            name='DVideo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(blank=True, max_length=250)),
                ('preview_url', models.CharField(blank=True, max_length=250)),
                ('is_visible', models.BooleanField(blank=True, default=False)),
                ('order_index', models.PositiveSmallIntegerField()),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'db_table': 'd_video',
                'default_related_name': 'd_videos',
            },
        ),
        migrations.CreateModel(
            name='DVideoGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
            ],
            options={
                'db_table': 'd_video_group',
                'default_related_name': 'd_video_groups',
            },
        ),
        migrations.CreateModel(
            name='DVideoLang',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('lang', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='d_video_langs', to='web_lib_core.Language')),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='d_video_langs', to='web_lib_core.DVideo')),
            ],
            options={
                'db_table': 'd_video_lang',
                'default_related_name': 'd_video_langs',
            },
        ),
        migrations.CreateModel(
            name='DVideoGroupLang',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('lang', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='d_video_group_langs', to='web_lib_core.Language')),
                ('video_group', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='d_video_group_langs', to='web_lib_core.DVideoGroup')),
            ],
            options={
                'db_table': 'd_video_group_lang',
                'default_related_name': 'd_video_group_langs',
            },
        ),
        migrations.AddField(
            model_name='dvideo',
            name='video_group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='d_videos', to='web_lib_core.DVideoGroup'),
        ),
        migrations.CreateModel(
            name='DMusicLang',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('singer', models.CharField(blank=True, max_length=64, null=True)),
                ('text', models.TextField(blank=True, null=True)),
                ('accord', models.TextField(blank=True, null=True)),
                ('lang', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='d_music_langs', to='web_lib_core.Language')),
                ('music', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='d_music_langs', to='web_lib_core.DMusic')),
            ],
            options={
                'db_table': 'd_music_lang',
                'default_related_name': 'd_music_langs',
            },
        ),
        migrations.CreateModel(
            name='DMusicGroupLang',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('lang', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='d_music_group_langs', to='web_lib_core.Language')),
                ('music_group', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='d_music_group_langs', to='web_lib_core.DMusicGroup')),
            ],
            options={
                'db_table': 'd_music_group_lang',
                'default_related_name': 'd_music_group_langs',
            },
        ),
        migrations.AddField(
            model_name='dmusic',
            name='music_group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='d_musics', to='web_lib_core.DMusicGroup'),
        ),
        migrations.CreateModel(
            name='DImageLang',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='d_image_langs', to='web_lib_core.DImage')),
                ('lang', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='d_image_langs', to='web_lib_core.Language')),
            ],
            options={
                'db_table': 'd_image_lang',
                'default_related_name': 'd_image_langs',
            },
        ),
        migrations.CreateModel(
            name='DImageGroupLang',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('image_group', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='d_image_group_langs', to='web_lib_core.DImageGroup')),
                ('lang', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='d_image_group_langs', to='web_lib_core.Language')),
            ],
            options={
                'db_table': 'd_image_group_lang',
                'default_related_name': 'd_image_group_langs',
            },
        ),
        migrations.AddField(
            model_name='dimage',
            name='image_group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='d_images', to='web_lib_core.DImageGroup'),
        ),
    ]