from rulemanager.rule.models import RuleGroup, Rules
import os
import json


def auto_insert_alert(tag, group):
    rule_list = []
    result = {}
    new_group = RuleGroup.objects.create(name=group, remarks="%s 系统自动导入" % group)
    alert_dir = os.path.dirname(__file__)
    alert_file = os.path.join(alert_dir, 'prometheus_alert.json')
    with open(alert_file, "r", encoding="utf8") as f:
        all_lines = json.load(f)
        for item in all_lines:
            if item['group'] == tag:
                rule = Rules(group=new_group, name=item['name'], rule=item['rule'], check_period=item['check_period'],
                             labels=item['labels'], description=item['description'], level=item['level'],
                             remarks=item['remarks'], alert_period=item['alert_period'], user="system")
                rule_list.append(rule)
    try:
        Rules.objects.bulk_create(rule_list)
        result['code'] = 0
    except Exception as e:
        result['code'] = 1
        result['err'] = e
        print(e)
    return result


def create_default_alert():
    result = {}
    group_list = {"base": "硬件指标", "bigdata": "大数据", "mysql": "mysql数据库", "k8s": 'k8s指标'}
    for tag, group in group_list.items():
        result = auto_insert_alert(tag, group)
    return result



