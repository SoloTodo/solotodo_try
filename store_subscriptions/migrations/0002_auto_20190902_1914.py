# Generated by Django 2.0.3 on 2019-09-02 19:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store_subscriptions', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='storesubscription',
            options={'ordering': ('-creation_date',), 'permissions': (['backend_list_store_subscriptions', 'Can see store subscription list in the backend'],)},
        ),
    ]