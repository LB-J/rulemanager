# Generated by Django 3.1.7 on 2021-04-22 02:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alert', '0010_auto_20210415_0623'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sendrecords',
            name='send_time',
            field=models.IntegerField(default=1619056918, verbose_name='send alert time'),
        ),
    ]
