# Generated by Django 4.1.7 on 2023-03-24 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_userexpand_erp_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='userexpand',
            name='alert_channel',
            field=models.IntegerField(choices=[(0, 'email'), (1, 'wechat'), (2, 'jd')], default=0, max_length=2, verbose_name='alert channel'),
        ),
    ]
