from django.db import models

# Create your models here.


class AlertReceivingGroup(models.Model):
    name = models.CharField(max_length=50, verbose_name="alert receiving group")
    remarks = models.CharField(max_length=200, verbose_name="group marks")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']


class AlertGroupTUsers(models.Model):
    user = models.ForeignKey('auth.User', related_name="alert_user", on_delete=models.CASCADE)
    group = models.ForeignKey('AlertReceivingGroup', related_name="alert_user_group", on_delete=models.CASCADE)

    class Meta:
        ordering = ['id']


class RuleGroup(models.Model):
    name = models.CharField(max_length=30, verbose_name="rule group name")
    remarks = models.CharField(max_length=200, verbose_name="rule group remarks")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']


class RuleGroupTAlertGroup(models.Model):
    rule_group = models.ForeignKey('RuleGroup', related_name="alert_groups", on_delete=models.CASCADE)
    alert_group = models.ForeignKey('AlertReceivingGroup', related_name='alert_group_rule', on_delete=models.CASCADE)

    class Meta:
        ordering = ['id']


class RuleGroupTAlertUser(models.Model):
    rule_group = models.ForeignKey('RuleGroup', related_name="alert_users", on_delete=models.CASCADE)
    alert_user = models.ForeignKey('auth.User', related_name='alert_user_for_rule', on_delete=models.CASCADE)

    class Meta:
        ordering = ['id']


class Rules(models.Model):
    group = models.ForeignKey('RuleGroup', verbose_name="rule group", related_name="rules_group", on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name="rule name")
    rule = models.CharField(max_length=250, verbose_name="alert rule")
    check_period = models.IntegerField(verbose_name="rule check time period")
    alert_period = models.IntegerField(default=5, verbose_name="alert send time period minute")
    labels = models.CharField(max_length=250, blank=True, default='', verbose_name="alert labels")
    # summary = models.CharField(max_length=250, default='', verbose_name="alert summary")
    description = models.CharField(max_length=250, default='', verbose_name="alert description")
    level = models.IntegerField(choices=((0, 'general'), (1, 'medium'), (2, 'serious')),
                                default=0, verbose_name="server status")
    user = models.CharField(max_length=100, verbose_name="create user")
    remarks = models.CharField(max_length=100, verbose_name="rule mark")
    status = models.BooleanField(default=True, verbose_name="if Disable")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="version create time")
    update_time = models.DateTimeField(auto_now=True, verbose_name="deploy or update time")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']


class RulesTAlertGroup(models.Model):
    rule = models.ForeignKey('Rules', related_name="rules_groups", on_delete=models.CASCADE)
    alert_group = models.ForeignKey('AlertReceivingGroup', related_name='alert_group_rules', on_delete=models.CASCADE)

    class Meta:
        ordering = ['id']


class RulesTAlertUsers(models.Model):
    rule = models.ForeignKey('Rules', related_name="rules_users", on_delete=models.CASCADE)
    alert_user = models.ForeignKey('auth.User', related_name='alert_user_for_rules', on_delete=models.CASCADE)

    class Meta:
        ordering = ['id']



