# Generated by Django 3.1.7 on 2021-04-29 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alert', '0013_auto_20210429_1651'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sendrecords',
            name='send_time',
            field=models.IntegerField(default=1619688446, verbose_name='send alert time'),
        ),
    ]
