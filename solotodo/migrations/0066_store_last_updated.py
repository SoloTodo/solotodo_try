# Generated by Django 2.2.13 on 2020-08-17 21:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solotodo', '0065_auto_20200817_2104'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='last_updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
