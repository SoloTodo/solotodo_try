# Generated by Django 2.0.3 on 2020-06-09 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solotodo', '0064_product_part_number'),
        ('microsite', '0005_auto_20200608_1815'),
    ]

    operations = [
        migrations.AddField(
            model_name='micrositebrand',
            name='stores',
            field=models.ManyToManyField(to='solotodo.Store'),
        ),
        migrations.AddField(
            model_name='micrositeentry',
            name='subtitle',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]
