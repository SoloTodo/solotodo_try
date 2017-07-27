# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-27 16:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('solotodo', '0015_storetype'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='storetype',
            options={'ordering': ('name',)},
        ),
        migrations.AlterField(
            model_name='store',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='solotodo.StoreType'),
        ),
    ]