from django.db import models
from django.utils import timezone
import time

# Create your models here.

# http://altermanager.prod.ntsyzl.com/api/v2/alerts


class AlertRecords(models.Model):
    alert_name = models.CharField(max_length=100, verbose_name="alert name")
    rule_id = models.IntegerField(verbose_name="rule id")
    host = models.CharField(max_length=100, default='', verbose_name="alert host")
    alert_uuid = models.CharField(max_length=100, default='', verbose_name="alert uuid")
    fingerprint = models.CharField(max_length=200, default='', verbose_name="alert fingerprint")
    description = models.CharField(max_length=250, default='', verbose_name="alert remark")
    status = models.IntegerField(choices=((1, "firing"), (2, 'resolved'), (3, 'delete'), (4, 'disable')), default=1,  verbose_name="receiver type")
    ack = models.IntegerField(choices=((0, 'yes'), (1, 'no')), default=1)
    if_send_resolved = models.IntegerField(choices=((0, 'yes'), (1, 'no')), default=1)
    alert_time = models.DateTimeField(default=timezone.now, verbose_name="alert time")
    resolved_time = models.DateTimeField(default=timezone.now, verbose_name="resolved time")


class AckRecords(models.Model):
    alert = models.CharField(max_length=24, verbose_name="alert id")
    ack = models.IntegerField(choices=((0, 'yes'), (1, 'no')))
    ack_mark = models.CharField(max_length=200, verbose_name=" ack commit")
    ack_time = models.DateTimeField(auto_now_add=True, verbose_name="ack time")


class SendRecords(models.Model):
    alert = models.CharField(max_length=24, verbose_name="alert id")
    alert_user = models.ForeignKey('auth.User', related_name="send_user", on_delete=models.CASCADE)
    times = models.IntegerField(verbose_name="alert send times", default=0)
    send_time = models.IntegerField(default=int(time.time()), verbose_name="send alert time")


class AlertHistory(models.Model):
    alert = models.CharField(max_length=24, verbose_name="alert id")
    name = models.CharField(max_length=100, verbose_name="alert name")
    rule_id = models.IntegerField(verbose_name="alert id")
    host = models.CharField(max_length=100, default='', verbose_name="alert host")
    status = models.IntegerField(choices=((1, "firing"), (2, 'resolved')), default=1,  verbose_name="receiver type")
    ack = models.IntegerField(choices=((0, 'yes'), (1, 'no')), default=1)
    alert_time = models.DateTimeField(default=timezone.now, verbose_name="alert  time")
    resolved_time = models.DateTimeField(default=timezone.now, verbose_name="resolved time")

