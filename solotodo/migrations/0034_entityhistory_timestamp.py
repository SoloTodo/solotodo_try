# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-15 12:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solotodo', '0033_auto_20170814_1209'),
    ]

    operations = [
        migrations.AddField(
            model_name='entityhistory',
            name='timestamp',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
