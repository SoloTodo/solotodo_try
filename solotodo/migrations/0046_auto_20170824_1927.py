# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-24 22:27
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('solotodo', '0045_auto_20170824_1842'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='entitylog',
            options={'ordering': ['-pk']},
        ),
    ]
