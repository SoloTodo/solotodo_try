# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-25 13:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solotodo', '0083_auto_20170925_0914'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApiClient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('url', models.URLField()),
            ],
            options={
                'permissions': [('view_api_client_entity_visits', 'View the entity visits associated to this API client')],
                'ordering': ('name',),
            },
        ),
    ]
