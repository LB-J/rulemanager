# Generated by Django 3.1.7 on 2021-03-31 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alert', '0002_sendrecords_send_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='alertrecords',
            name='resolved_time',
        ),
        migrations.RemoveField(
            model_name='alertrecords',
            name='trigger_time',
        ),
        migrations.AddField(
            model_name='alertrecords',
            name='create_time',
            field=models.DateTimeField(auto_now=True, verbose_name='alert resolved time'),
        ),
        migrations.AddField(
            model_name='alertrecords',
            name='type',
            field=models.IntegerField(choices=[(0, 'trigger'), (1, 'resloved')], default=0, verbose_name='receiver type'),
        ),
    ]
