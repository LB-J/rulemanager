# Generated by Django 3.1.7 on 2021-04-26 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alert', '0011_auto_20210422_0201'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sendrecords',
            name='send_time',
            field=models.IntegerField(default=1619430987, verbose_name='send alert time'),
        ),
    ]
