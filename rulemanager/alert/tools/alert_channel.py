# -*- coding: utf-8 -*-
import hashlib
import time

import requests
import json
import smtplib
from django.core.cache import cache
import logging
import os
from rulemanager import settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rulemanager.settings')


def send_mail_icity(user, subject, ms):
    mail_host = settings.SMTP_MAIL
    mail_user = settings.USER_MAIL
    login_pass = settings.PASSWORD_MAIL
    new_msg = "Content-Type: text/plain; charset=\"utf-8\"\r\nSubject: %s\r\nFrom: op@icity-jd.com\r\nTo: %s\r\n\r\n%s" % (subject, ";".join(user), ms)
    # print(new_msg)
    try:
        mail_send = smtplib.SMTP(host=mail_host)
        mail_send.login(mail_user, login_pass)
        mail_send.sendmail(mail_user, user, new_msg.strip().encode("utf-8"))
        mail_send.quit()
    except smtplib.SMTPException as e:
        logging.error("[+]sed mail failed %s" % e)


def generate_token():
    # 企业ID
    corpid = settings.wx_corp_id
    # 运维告警平台
    corpsecret = settings.wx_corp_secret
    url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=%s&corpsecret=%s" % (corpid, corpsecret)
    req = requests.get(url)
    result = req.json()
    if result["errcode"] == 0:
        cache.set("wx_access_token", result["access_token"], timeout=7100)
        return True
    else:
        logging.error("[+]get wx access token error:%s" % result["errmsg"])
        return False


def send_wx(msg, user_list):
    expire_time = cache.ttl("wx_access_token")
    if expire_time == 0:
        generate_token()
    wx_token = cache.get("wx_access_token")
    url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=%s" % wx_token
    params = {
            "touser": user_list,
            "msgtype": "text",
            "agentid": settings.wx_agent_id,
            "text": {
                "content": msg
            },
            "safe": 0
    }
    req = requests.post(url, data=json.dumps(params))
    print(req.json())


##此处为内部聊天工具发送模块。不对外提供服务
def send_dongdong(msg, user_list):
    project = settings.dd_project
    security = settings.dd_security
    fmt = "%Y%m%d%H%M%S"
    timestamp = time.strftime(fmt, time.localtime(time.time()))
    sign = project + '=' + security + '=' + timestamp
    hash_sign = hashlib.md5(sign.encode(encoding='UTF-8')).hexdigest()
    req_url = settings.dd_url + msg + '&sign=' + hash_sign + '&project=' + project + '&timestamp=' + timestamp
    params = {
        "appName": settings.dd_appName,
        "ruleKey": "监控告警",
        "recipientWay": "MSG",
        "recipients": user_list
    }
    header = {
        'Content-Type': 'application/json'
    }
    req_result = requests.post(req_url, data=json.dumps(params), headers=header)
    result = req_result.text
    if result.lower() != "success":
        logging.error("send message to dd failed ,return result:%s" % result)
    else:
        logging.info("send message success")




