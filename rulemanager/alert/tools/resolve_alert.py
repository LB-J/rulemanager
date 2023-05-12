import json
from rulemanager.alert.models import *
from rulemanager.rule.models import *
import logging
import time
from datetime import datetime
from rulemanager.alert.tools import check_alert
import uuid
from rulemanager.user.models import UserExpand
import pytz
from rulemanager.alert.tools import alert_channel


# 存到redis里？快速查询，在新建用户和用户组时，更新redis数据
# 这里根据用户名和用户分组从 redis 获取数据
# 每次启动自动更新 redis 数据
def get_rule_user(rule):
    alter_user = []
    # 规则对应的告警接收分组
    # b = RulesTAlertGroup.objects.filter(rule=rule)
    b = RuleGroupTAlertGroup.objects.filter(rule_group=rule.group)
    alter_user.extend([i['user'] for i in
                       AlertGroupTUsers.objects.filter(group__pk__in=[i.alert_group.pk for i in b]).values(
                           'user').distinct()])
    alter_user.extend(
        [i['alert_user'] for i in RulesTAlertUsers.objects.filter(rule=rule).values('alert_user').distinct()])
    user_list = list(set(alter_user))
    user = UserExpand.objects.filter(user_id__in=user_list)
    return user


# 生成告警唯一标识
def generate_uuid(start_time, fingerprint):
    # unix_time = datetime.timestamp(datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%S.%f%WZ"))
    uuid_code = uuid.uuid3(uuid.NAMESPACE_X500, "%s-%s" % (fingerprint, str(start_time)))
    return uuid_code


def calculation_duration(start_time, end_time=None):
    china = pytz.timezone('Asia/Shanghai')
    utc = pytz.timezone('UTC')
    start_date = start_time.replace(tzinfo=utc).astimezone(china)
    if end_time is None:
        end_date = datetime.now().astimezone()
    else:
        end_date = end_time.replace(tzinfo=utc).astimezone(china)
    duration = (end_date - start_date)
    day = duration.days
    hour = duration.seconds // 3600
    minute = duration.seconds % 60
    return day, hour, minute


# 告警记录中的时间转换为东八区
def format_date(date):
    china = pytz.timezone('Asia/Shanghai')
    utc = pytz.timezone('UTC')
    new = date.replace(tzinfo=utc).astimezone(china)
    return new


# 保存告警到实时库中
def save_db(data):
    if "rule_id" not in data['groupLabels'].keys():
        rule_id = int(data['groupLabels']['alertid'])
    else:
        rule_id = int(data['groupLabels']['rule_id'])
    alert_name = data['commonLabels']['alertname']
    alert_list = data['alerts']
    resolved_alert = []
    new_alert = []
    all_alert = []
    for i in alert_list:
        alert_uuid = generate_uuid(start_time=i["startsAt"], fingerprint=i['fingerprint'])
        alert = AlertRecords.objects.filter(alert_uuid=alert_uuid)
        # check recovery
        if len(alert) == 1 and i['status'] == "resolved":
            # (1, "firing"), (2, 'resolved')
            alert.update(status=2, resolved_time=i['endsAt'])
            resolved_alert.append(alert_uuid)
        elif len(alert) == 0 and i['status'] == "firing":
            AlertRecords.objects.create(alert_name=alert_name, rule_id=rule_id, status=1,
                                        host=i['labels']['alert_host'], alert_time=i["startsAt"],
                                        description=i['annotations']['description'], alert_uuid=alert_uuid,
                                        fingerprint=i['fingerprint'])
            # SendRecords.objects.create()
            new_alert.append(alert_uuid)
        elif len(alert) == 1 and i['status'] == "firing":
            alert.update(status=1)
            all_alert.append(alert_uuid)
        elif len(alert) > 1:
            logging.warning("[+] This has a alert have too many records. ID:%d" % alert_uuid)
    all_alert.extend(new_alert)
    schedule = check_alert.scheduler
    if len(new_alert) > 0 or len(resolved_alert) > 0:
        get_all_alert(rule_id=rule_id, all_alert=all_alert, new_alert=new_alert, resolved_alert=resolved_alert)
    elif len(all_alert) == 0 and schedule.get_job("send_alert_%d" % rule_id, "default"):
        schedule.remove_job("send_alert_%d" % rule_id, "default")
    else:
        logging.info("[+] not change!")


def print_alert(rule, user_list, alert_list, resolved_uuid):
    start_time = time.time()
    user_wechat_list = []
    user_email_list = []
    user_phone_list = []
    user_erp_list = []
    for i in user_list:
        if i.alert_channel == 0:
            user_email_list.append(i.user.email)
        elif i.alert_channel == 1:
            user_wechat_list.append(i.user.email)
        elif i.alert_channel == 2:
            user_erp_list.append(i.erp_id)
        user_phone_list.append(i.phone)

    print("告警接收用户：%s" % user_wechat_list)
    print("告警接收用户电话：%s" % ','.join(user_phone_list))
    print("告警接收用户邮件：%s" % ','.join(user_email_list))
    now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    print("告警时间：%s\n" % now)
    print("告警名称：%s" % rule.name)
    message = ""
    if_need_send = False
    if len(resolved_uuid) > 0:
        recover_alert = AlertRecords.objects.filter(alert_uuid__in=resolved_uuid, if_send_resolved=1)
        if len(recover_alert) == 0:
            logging.info("[+] not recover list")
        else:
            message = message + "恢复列表:\n"
            if_need_send = True
            for i in recover_alert:
                day, hour, minute = calculation_duration(start_time=i.alert_time, end_time=i.resolved_time)
                message = message + "告警描述：%s\n告警主机：%s\n触发时间：%s\n恢复时间：%s\n持续时间：%dd%dh%dm\n" % \
                          (i.description, i.host, format_date(i.alert_time), format_date(i.resolved_time), day, hour,
                           minute)
            # 发送恢复之后，将状态置为已发送恢复
            recover_alert.update(if_send_resolved=0)
    if len(alert_list) > 0:
        need_send_alert = AlertRecords.objects.filter(alert_uuid__in=alert_list, status=1, ack=1)
        if len(need_send_alert) == 0:
            logging.info("[+] not problem send")
        else:
            if_need_send = True
            message = message + "告警列表:\n"
            for i in need_send_alert:
                day, hour, minute = calculation_duration(start_time=i.alert_time)
                message = message + "告警描述：%s\n告警主机：%s\n触发时间：%s\n持续时间：%dd%dh%dm\n" % \
                          (i.description, i.host, format_date(i.alert_time), day, hour, minute)
    if if_need_send:
        alert_channel.send_mail_icity(user=user_email_list, subject=rule.name, ms=message)
        alert_channel.send_wx(msg=message, user_list=user_wechat_list)
        alert_channel.send_dongdong(msg=message, user_list=user_erp_list)
    end_time = time.time()
    exec_time = int(end_time - start_time)
    print("[+] %s" % message)
    print("[+]执行时间：%d" % exec_time)


# 删除异常任务
def delete_job(rule_id):
    schedule = check_alert.scheduler
    job = schedule.get_job("send_alert_%d" % rule_id, "default")
    if job:
        schedule.remove_job("send_alert_%d" % rule_id, "default")


# 增加update，变更告警通知时间，需要更新job的执行周期
def get_all_alert(rule_id, all_alert, new_alert, resolved_alert):
    schedule = check_alert.scheduler
    try:
        rule = Rules.objects.get(id=rule_id)
    except Exception as e:
        logging.warning("this rule not exits")
        delete_job(rule_id)
        return
    user = get_rule_user(rule=rule)
    job = schedule.get_job("send_alert_%d" % rule_id, "default")
    # if len(new_alert) > 0 or (len(resolved_alert) > 0):
    if job:
        schedule.remove_job("send_alert_%d" % rule_id, "default")
    if len(resolved_alert) > 0 and all_alert == 0:
        schedule.add_job(print_alert, 'interval',
                         kwargs={"rule": rule, "resolved_uuid": resolved_alert, "alert_list": all_alert,
                                 "user_list": user},
                         id="send_alert_%d" % rule_id,
                         name="send_alert for %d" % rule_id,
                         jobstore="default",
                         executor="default",
                         replace_existing=True)
    elif len(new_alert) > 0 or len(resolved_alert) > 0:
        schedule.add_job(print_alert, 'interval',
                         kwargs={"rule": rule, "resolved_uuid": resolved_alert, "alert_list": all_alert,
                                 "user_list": user},
                         id="send_alert_%d" % rule_id,
                         name="send_alert for %d" % rule_id,
                         jobstore="default",
                         executor="default",
                         misfire_grace_time=60,
                         max_instances=1,
                         seconds=rule.alert_period * 60,
                         next_run_time=datetime.now(),
                         replace_existing=True)
    else:
        pass
