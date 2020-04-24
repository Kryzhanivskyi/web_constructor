# Generated by Django 3.0.2 on 2020-02-14 12:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web_lib_core', '0005_auto_20200213_1711'),
    ]

    operations = [
        migrations.CreateModel(
            name='PageLang',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=128, null=True)),
                ('description', models.CharField(blank=True, max_length=1024, null=True)),
                ('keywords', models.CharField(blank=True, max_length=1024, null=True)),
                ('lang', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='page_langs', to='web_lib_core.Language')),
                ('page', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='page_langs', to='web_lib_core.Page')),
            ],
            options={
                'db_table': 'page_lang',
                'default_related_name': 'page_langs',
            },
        ),
    ]
