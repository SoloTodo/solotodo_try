# Generated by Django 2.0.3 on 2019-04-16 19:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('brand_comparisons', '0004_auto_20190408_2051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brandcomparisonsegmentrow',
            name='product_1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='product_1', to='solotodo.Product'),
        ),
        migrations.AlterField(
            model_name='brandcomparisonsegmentrow',
            name='product_2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='product_2', to='solotodo.Product'),
        ),
    ]
