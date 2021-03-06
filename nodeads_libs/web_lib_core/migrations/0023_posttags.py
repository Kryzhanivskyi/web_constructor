# Generated by Django 3.0.2 on 2020-03-23 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_lib_core', '0022_dposttaglang'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostTags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('groupid', models.IntegerField(blank=True, null=True)),
                ('name', models.CharField(blank=True, max_length=64, null=True)),
                ('url', models.CharField(blank=True, max_length=64, null=True)),
                ('sitemapenable', models.SmallIntegerField(blank=True, null=True)),
                ('apiappexpose', models.SmallIntegerField()),
                ('urlprefix', models.CharField(blank=True, max_length=256, null=True)),
                ('language_id', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'post_tags',
                'managed': False,
            },
        ),
    ]
