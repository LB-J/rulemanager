# Generated by Django 3.1.7 on 2021-04-29 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rule', '0004_rules_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rules',
            name='status',
            field=models.BooleanField(default=True, verbose_name='if Disable'),
        ),
    ]
