# Generated by Django 3.1.7 on 2021-04-12 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alert', '0006_auto_20210412_0250'),
    ]

    operations = [
        migrations.AddField(
            model_name='alertrecords',
            name='description',
            field=models.CharField(default='', max_length=250, verbose_name='alert remark'),
        ),
    ]
