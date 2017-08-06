# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-06 15:04
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('solotodo', '0020_auto_20170731_1754'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='store',
            options={'ordering': ['name'], 'permissions': (['view_store', 'Can view store'], ['update_store_prices', 'Can update store'], ['backend_list_stores', 'Can access store list in backend'], ['view_store_update_logs', 'Can view store update logs'])},
        ),
    ]
