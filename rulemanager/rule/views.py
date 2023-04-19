import logging


from django_filters.rest_framework import DjangoFilterBackend
import django_filters
from rest_framework_bulk import BulkModelViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions, AllowAny
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rulemanager.rule.serializers import *
from rulemanager.rule.models import *
from rulemanager.rule.utils import  init_rule
from rulemanager.alert.tools import check_alert
from rulemanager.alert.models import AlertRecords


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000


class AlertReceivingGroupFilter(django_filters.rest_framework.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = AlertReceivingGroup
        fields = "__all__"


class AlertReceivingGroupViewSet(viewsets.ModelViewSet):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (AllowAny,)
    queryset = AlertReceivingGroup.objects.all().order_by('-id')
    serializer_class = AlertReceivingGroupSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    filter_class = AlertReceivingGroupFilter
    pagination_class = StandardResultsSetPagination


class AlertGroupTUsersFilter(django_filters.rest_framework.FilterSet):
    class Meta:
        model = AlertGroupTUsers
        fields = "__all__"


class AlertGroupTUsersViewSet(BulkModelViewSet):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (AllowAny,)
    queryset = AlertGroupTUsers.objects.all().order_by('-id')
    serializer_class = AlertGroupTUsersSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    filter_class = AlertGroupTUsersFilter
    pagination_class = StandardResultsSetPagination


class RuleGroupFilter(django_filters.rest_framework.FilterSet):
    class Meta:
        model = RuleGroup
        fields = "__all__"


class RuleGroupViewSet(viewsets.ModelViewSet):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (AllowAny,)
    queryset = RuleGroup.objects.all().order_by('-id')
    serializer_class = RuleGroupSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    filter_class = RuleGroupFilter
    pagination_class = StandardResultsSetPagination


class RuleGroupTAlertGroupFilter(django_filters.rest_framework.FilterSet):
    class Meta:
        model = RuleGroupTAlertGroup
        fields = "__all__"


def add_rules_group(rule_group, alert_group):
    all_rule = Rules.objects.filter(group=rule_group)
    group_list = [RulesTAlertGroup(rule=i, alert_group_id=alert_group) for i in all_rule]
    RulesTAlertGroup.objects.bulk_create(group_list)


def delete_rules_group(rule_group, alert_group):
    all_rule = Rules.objects.filter(group=rule_group).values('id')
    RulesTAlertGroup.objects.filter(rule_id__in=all_rule, alert_group_id=alert_group).delete()


class RuleGroupTAlertGroupViewSet(BulkModelViewSet):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (AllowAny,)
    queryset = RuleGroupTAlertGroup.objects.all().order_by('-id')
    serializer_class = RuleGroupTAlertGroupSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    filter_class = RuleGroupTAlertGroupFilter
    pagination_class = StandardResultsSetPagination

    def perform_create(self, serializer):
        s = serializer.save()
        if type(s) is list:
            for i in s:
                add_rules_group(i.rule_group, i.alert_group)
        else:
            add_rules_group(s.rule_group, s.alert_group)

    def perform_destroy(self, instance):
        delete_rules_group(instance.rule_group, instance.alert_group)
        instance.delete()


class RuleGroupTAlertUserFilter(django_filters.rest_framework.FilterSet):
    class Meta:
        model = RuleGroupTAlertUser
        fields = "__all__"


def add_rules_user(rule_group, alert_user):
    all_rule = Rules.objects.filter(group=rule_group)
    user_list = [RulesTAlertUsers(rule=i, alert_user=alert_user) for i in all_rule]
    RulesTAlertUsers.objects.bulk_create(user_list)


def delete_rules_user(rule_group, alert_user):
    all_rule = Rules.objects.filter(group=rule_group).values('id')
    RulesTAlertUsers.objects.filter(rule_id__in=all_rule, alert_user=alert_user).delete()


class RuleGroupTAlertUserViewSet(BulkModelViewSet):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (AllowAny,)
    queryset = RuleGroupTAlertUser.objects.all().order_by('-id')
    serializer_class = RuleGroupTAlertUserSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    filter_class = RuleGroupTAlertUserFilter
    pagination_class = StandardResultsSetPagination

    def perform_create(self, serializer):
        s = serializer.save()
        if type(s) is list:
            for i in s:
                add_rules_user(i.rule_group, i.alert_user)
        else:
            add_rules_user(s.rule_group, s.alert_user)

    def perform_destroy(self, instance):
        delete_rules_user(instance.rule_group, instance.alert_user)
        instance.delete()


class RulesFilter(django_filters.rest_framework.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Rules
        fields = "__all__"


def add_rule_group(group, rule):
    alert_group = RuleGroupTAlertGroup.objects.filter(rule_group_id=group).values('alert_group')
    add_group = []
    for i in alert_group:
        add_group.append(RulesTAlertGroup(rule_id=rule, alert_group_id=i['alert_group']))
    if len(add_group) > 0:
        RulesTAlertGroup.objects.bulk_create(add_group)


class RulesViewSet(viewsets.ModelViewSet):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (AllowAny,)
    queryset = Rules.objects.all().order_by('-id')
    serializer_class = RulesSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    filter_class = RulesFilter
    pagination_class = StandardResultsSetPagination

    def perform_create(self, serializer):
        s = serializer.save()
        rule_group = s.group.id
        add_rule_group(group=rule_group, rule=s.id)

    def perform_update(self, serializer):
        s = serializer.save()
        task = check_alert.scheduler
        # print(s.id, s.alert_period)
        f = task.get_job(job_id="send_alert_%d" % s.id, jobstore="default")
        # print(f)
        if f:
            task.remove_job(job_id="send_alert_%d" % s.id, jobstore="default")
        if s.status is False:
            # status 4 disable
            AlertRecords.objects.filter(rule_id=s.id).update(status=4)

    def perform_destroy(self, instance):
        # status 3 delete
        AlertRecords.objects.filter(rule_id=instance.id).update(status=3)
        task = check_alert.scheduler
        f = task.get_job(job_id="send_alert_%d" % instance.id, jobstore="default")
        if f:
            task.remove_job(job_id="send_alert_%d" % instance.id, jobstore="default")
        instance.delete()


class RulesTAlertGroupFilter(django_filters.rest_framework.FilterSet):
    class Meta:
        model = RulesTAlertGroup
        fields = "__all__"


class RulesTAlertGroupViewSet(BulkModelViewSet):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (AllowAny,)
    queryset = RulesTAlertGroup.objects.all().order_by('-id')
    serializer_class = RulesTAlertGroupSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    filter_class = RulesTAlertGroupFilter
    pagination_class = StandardResultsSetPagination


class RulesTAlertUsersFilter(django_filters.rest_framework.FilterSet):
    class Meta:
        model = RulesTAlertUsers
        fields = "__all__"


class RulesTAlertUsersViewSet(BulkModelViewSet):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (AllowAny,)
    queryset = RulesTAlertUsers.objects.all().order_by('-id')
    serializer_class = RulesTAlertUsersSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    filter_class = RulesTAlertUsersFilter
    pagination_class = StandardResultsSetPagination


'''
Add {
name: '',
remarks: '',
alert_groups: [],
}

update {
id: '',
alert_groups: [],
}
'''


class RuleGroupAdd(APIView):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (AllowAny,)

    def post(self, request):
        data = request.data
        result = {}
        try:
            new_rule_group = RuleGroup.objects.create(name=data['name'], remarks=data['remarks'])
            new_alert_group = []
            for group in data['alert_groups']:
                new_alert_group.append(RuleGroupTAlertGroup(alert_group_id=group, rule_group_id=new_rule_group.id))
                add_rules_group(rule_group=new_rule_group.id, alert_group=group)
            if len(new_alert_group) > 0:
                RuleGroupTAlertGroup.objects.bulk_create(new_alert_group)
            result['code'] = 0
        except Exception as e:
            result['code'] = 1
            logging.error("[+] add new group error%s" % e)
        return Response(status=status.HTTP_200_OK, data=result)

    def put(self, request, pk):
        result = {}
        data = request.data
        rule_group_id = pk
        update_group = data['alert_groups']
        add_alert_group = []
        try:
            old_alert_group = RuleGroupTAlertGroup.objects.filter(rule_group_id=rule_group_id).values('alert_group')
            old_alert_group_list = [i['alert_group'] for i in old_alert_group]
            new_alert_group = list(set(update_group).difference(set(old_alert_group_list)))
            delete_alert_group = list(set(old_alert_group_list).difference(set(update_group)))
            if len(new_alert_group) > 0:
                print(new_alert_group)
                for g in new_alert_group:
                    add_alert_group.append(RuleGroupTAlertGroup(alert_group_id=g, rule_group_id=rule_group_id))
                    add_rules_group(rule_group=rule_group_id, alert_group=g)
                RuleGroupTAlertGroup.objects.bulk_create(add_alert_group)
            if len(delete_alert_group) > 0:
                RuleGroupTAlertGroup.objects.filter(rule_group_id=rule_group_id, alert_group_id__in=delete_alert_group).delete()
                for g in delete_alert_group:
                    delete_rules_group(rule_group=rule_group_id, alert_group=g)
            result['code'] = 0
        except Exception as e:
            logging.error("[+] update user group failed:%s" % e)
            result['code'] = 1
        return Response(status=status.HTTP_200_OK, data=result)

    def delete(self, request):
        pass


#  维护规则和用户之间的关系
'''
data = {
id: '',
user_list: ''
}
'''


class RuleUserAdd(APIView):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (AllowAny,)

    def post(self, request):
        data = request.data
        result = {}
        rule_id = data['id']
        user_list = data['user_list']
        try:
            res1 = RulesTAlertUsers.objects.filter(rule_id=rule_id).values('alert_user')
            old_user_list = [i['alert_user'] for i in res1]
            new_user = list(set(user_list).difference(set(old_user_list)))
            delete_user = list(set(old_user_list).difference(set(user_list)))
            if len(new_user) > 0:
                add_group = [RulesTAlertUsers(alert_user_id=i, rule_id=rule_id) for i in new_user]
                RulesTAlertUsers.objects.bulk_create(add_group)
            if len(delete_user) > 0:
                RulesTAlertUsers.objects.filter(rule_id=rule_id, alert_user__in=delete_user).delete()
            result['code'] = 0
        except Exception as e:
            logging.error("[+] add rule user failed:%s" % e)
            print(e)
            result['code'] = 1
        return Response(status=status.HTTP_200_OK, data=result)

    # 直接删除所有关联的规则用户信息
    # def delete(self,request, pk):


# 更新规则状态
# data = {rule_id:, status: }
#
#
class UpdateRuleStatus(APIView):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (AllowAny,)

    def post(self, request):
        data = request.data
        task = check_alert.scheduler
        result = {}
        try:
            Rules.objects.filter(id=data['rule_id']).update(status=data['status'])
            # 当规则禁用的时候，删除正在发生的定时任务
            if data['status'] is False:
                AlertRecords.objects.filter(rule_id=data['rule_id']).update(status=4)
                f = task.get_job(job_id="send_alert_%d" % data['rule_id'], jobstore="default")
                if f:
                    task.remove_job(job_id="send_alert_%d" % data['rule_id'], jobstore="default")
            result['code'] = 0
        except Exception as e:
            logging.error('[+] update rule status failed:%s ' % e)
            result['code'] = 1
        return Response(status=status.HTTP_200_OK, data=result)


class AutoDefaultAlert(APIView):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (AllowAny,)

    def post(self, data):
        print(data)
        result = init_rule.create_default_alert()
        return Response(status=status.HTTP_200_OK, data=result)


