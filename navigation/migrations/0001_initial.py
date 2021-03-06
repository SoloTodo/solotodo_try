# Generated by Django 2.0 on 2018-01-26 15:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('solotodo', '0017_country_flag'),
    ]

    operations = [
        migrations.CreateModel(
            name='NavDepartment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('ordering', models.IntegerField()),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='solotodo.Country')),
            ],
            options={
                'ordering': ['country', 'ordering'],
            },
        ),
        migrations.CreateModel(
            name='NavItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('ordering', models.IntegerField()),
            ],
            options={
                'ordering': ['section', 'ordering'],
            },
        ),
        migrations.CreateModel(
            name='NavSection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('ordering', models.IntegerField()),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='navigation.NavDepartment')),
            ],
            options={
                'ordering': ['department', 'ordering'],
            },
        ),
        migrations.AddField(
            model_name='navitem',
            name='section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='navigation.NavSection'),
        ),
    ]
