# Generated by Django 3.1.7 on 2021-04-12 02:50

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('alert', '0005_auto_20210401_0621'),
    ]

    operations = [
        migrations.CreateModel(
            name='AlertHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alert', models.CharField(max_length=24, verbose_name='alert id')),
                ('name', models.CharField(max_length=100, verbose_name='alert name')),
                ('rule_id', models.IntegerField(verbose_name='alert id')),
                ('host', models.CharField(default='', max_length=100, verbose_name='alert host')),
                ('status', models.IntegerField(choices=[(1, 'firing'), (2, 'resolved')], default=1, verbose_name='receiver type')),
                ('ack', models.IntegerField(choices=[(0, 'yes'), (1, 'no')], default=1)),
                ('alert_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='alert  time')),
                ('resolved_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='resolved time')),
            ],
        ),
        migrations.RenameField(
            model_name='alertrecords',
            old_name='alert_id',
            new_name='rule_id',
        ),
        migrations.RemoveField(
            model_name='alertrecords',
            name='create_time',
        ),
        migrations.RemoveField(
            model_name='alertrecords',
            name='if_send',
        ),
        migrations.RemoveField(
            model_name='alertrecords',
            name='type',
        ),
        migrations.AddField(
            model_name='alertrecords',
            name='ack',
            field=models.IntegerField(choices=[(0, 'yes'), (1, 'no')], default=1),
        ),
        migrations.AddField(
            model_name='alertrecords',
            name='alert_time',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='alert time'),
        ),
        migrations.AddField(
            model_name='alertrecords',
            name='resolved_time',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='resolved time'),
        ),
        migrations.AddField(
            model_name='alertrecords',
            name='status',
            field=models.IntegerField(choices=[(1, 'firing'), (2, 'resolved')], default=1, verbose_name='receiver type'),
        ),
        migrations.AddField(
            model_name='sendrecords',
            name='times',
            field=models.IntegerField(default=0, verbose_name='alert send times'),
        ),
        migrations.AlterField(
            model_name='ackrecords',
            name='alert',
            field=models.CharField(max_length=24, verbose_name='alert id'),
        ),
        migrations.AlterField(
            model_name='sendrecords',
            name='alert',
            field=models.CharField(max_length=24, verbose_name='alert id'),
        ),
    ]