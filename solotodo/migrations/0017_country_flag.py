# Generated by Django 2.0 on 2018-01-22 18:15

from django.db import migrations
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('solotodo', '0016_auto_20180119_1827'),
    ]

    operations = [
        migrations.AddField(
            model_name='country',
            name='flag',
            field=sorl.thumbnail.fields.ImageField(default='flag.jpg', upload_to='country_flags'),
            preserve_default=False,
        ),
    ]
