# Generated by Django 5.1.4 on 2024-12-06 00:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='property',
            name='address',
        ),
        migrations.RemoveField(
            model_name='property',
            name='number_of_units',
        ),
        migrations.AddField(
            model_name='property',
            name='cluster',
            field=models.CharField(default='DefaultCluster', max_length=50),
        ),
        migrations.AddField(
            model_name='property',
            name='floors',
            field=models.CharField(choices=[('2', '2 floors'), ('3', '3 floors')], default='2', max_length=10),
        ),
        migrations.AddField(
            model_name='property',
            name='status',
            field=models.CharField(default='Vacant', max_length=50),
        ),
        migrations.AddField(
            model_name='property',
            name='type',
            field=models.CharField(choices=[('Major', 'Major'), ('Minor', 'Minor')], default='Major', max_length=10),
        ),
        migrations.AddField(
            model_name='property',
            name='villa',
            field=models.CharField(default='DefaultVilla', max_length=50),
        ),
    ]
