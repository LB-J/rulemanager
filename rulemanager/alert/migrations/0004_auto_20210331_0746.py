# Generated by Django 3.1.7 on 2021-03-31 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alert', '0003_auto_20210331_0700'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alertrecords',
            name='type',
            field=models.CharField(max_length=30, verbose_name='receiver type'),
        ),
    ]
