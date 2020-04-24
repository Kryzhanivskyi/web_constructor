# Generated by Django 3.0.2 on 2020-03-23 14:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web_lib_core', '0021_auto_20200305_1504'),
    ]

    operations = [
        migrations.CreateModel(
            name='DPostTagLang',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('lang', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='d_post_tag_langs', to='web_lib_core.Language')),
                ('post_tag', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='d_post_tag_langs', to='web_lib_core.DPostTag')),
            ],
            options={
                'db_table': 'd_post_tag_lang',
                'default_related_name': 'd_post_tag_langs',
            },
        ),
    ]
