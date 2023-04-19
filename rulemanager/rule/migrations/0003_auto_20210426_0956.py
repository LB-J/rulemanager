# Generated by Django 3.1.7 on 2021-04-26 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rule', '0002_rules_alert_period'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rules',
            name='summary',
        ),
        migrations.AlterField(
            model_name='rules',
            name='description',
            field=models.CharField(default='', max_length=250, verbose_name='alert description'),
        ),
        migrations.AlterField(
            model_name='rules',
            name='labels',
            field=models.CharField(blank=True, default='', max_length=250, verbose_name='alert labels'),
        ),
    ]
