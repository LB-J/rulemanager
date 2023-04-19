import json
import logging
import sys
from rulemanager.alert.serializers import *
from rulemanager.rule.models import AlertReceivingGroup, AlertGroupTUsers, Rules
from django_filters.rest_framework import DjangoFilterBackend
import django_filters
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions, AllowAny
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rulemanager.alert.tools import resolve_alert
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rulemanager.alert.tools import check_alert


class WebHook(APIView):
    authentication_classes = (SessionAuthentication, TokenAuthentication,)
    permission_classes = (AllowAny, )

    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        resolve_alert.save_db(data)
        return Response(status=status.HTTP_200_OK)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000


class AlertRecordsFilter(django_filters.rest_framework.FilterSet):
    host = django_filters.CharFilter(lookup_expr='icontains')
    alert_name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = AlertRecords
        fields = "__all__"


class AlertRecordsViewSet(viewsets.ModelViewSet):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (AllowAny,)
    queryset = AlertRecords.objects.all().order_by('-id')
    serializer_class = AlertRecordsSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    filter_class = AlertRecordsFilter
    pagination_class = StandardResultsSetPagination


class AckRecordsFilter(django_filters.rest_framework.FilterSet):
    class Meta:
        model = AlertRecords
        fields = "__all__"


class AckRecordsViewSet(viewsets.ModelViewSet):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (AllowAny,)
    queryset = AckRecords.objects.all().order_by('-id')
    serializer_class = AckRecordsSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    filter_class = AckRecordsFilter
    pagination_class = StandardResultsSetPagination


class SendRecordsFilter(django_filters.rest_framework.FilterSet):
    class Meta:
        model = SendRecords
        fields = "__all__"


class SendRecordsViewSet(viewsets.ModelViewSet):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (AllowAny,)
    queryset = SendRecords.objects.all().order_by('-id')
    serializer_class = SendRecordsSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    filter_class = SendRecordsFilter
    pagination_class = StandardResultsSetPagination


'''
new  {
name: ''
remarks: '',
user: []
}
update {
group: ''
user: []
}
'''


class AddGroup(APIView):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (AllowAny,)

    def post(self, request):
        data = request.data
        result = {}
        try:
            new_group = AlertReceivingGroup.objects.create(name=data['name'], remarks=data['remarks'])
            new_relate = []
            for u in data['user']:
                new_relate.append(AlertGroupTUsers(user_id=u, group_id=new_group.id))
            if len(new_relate) > 0:
                AlertGroupTUsers.objects.bulk_create(new_relate)
            result['code'] = 0
        except Exception as e:
            result['code'] = 1
            logging.error("[+] add new group error%s" % e)

        return Response(status=status.HTTP_200_OK, data=result)

    def put(self, request, pk):
        result = {}
        data = request.data
        group_id = pk
        update_user = data['user']
        try:
            old_user = AlertGroupTUsers.objects.filter(group_id=group_id).values('user')
            old_list = [i['user'] for i in old_user]
            new_user = list(set(update_user).difference(set(old_list)))
            delete_user = list(set(old_list).difference(set(update_user)))
            if len(new_user) > 0:
                add_group = [AlertGroupTUsers(user_id=i, group_id=group_id) for i in new_user]
                AlertGroupTUsers.objects.bulk_create(add_group)
            if len(delete_user) > 0:
                AlertGroupTUsers.objects.filter(user_id__in=delete_user, group_id=group_id).delete()
            result['code'] = 0
        except Exception as e:
            logging.error("[+] update user group failed:%s" % e)
            result['code'] = 1
        return Response(status=status.HTTP_200_OK, data=result)



# ack alert
'''
data = {
alert_id: []
}
 # alert list 
'''


class AckAlert(APIView):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (AllowAny,)

    def post(self, request):
        result = {}
        alert = request.data
        try:
            alert_list = alert['alert_id']
            AlertRecords.objects.filter(id__in=alert_list).update(ack=0)
            result['code'] = 0
        except Exception as e:
            result['code'] = 1
            logging.error("[+] ack alert failed:%s" % e)
        return Response(status=status.HTTP_200_OK, data=result)

#
# # 获取当前实时告警内容
# class QueryCurrentAlert(APIView):


# 获取当前调度任务列表，以及删除或暂停
class SchedulerTask(APIView):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (AllowAny,)

    # 获取当前队列任务
    def get(self, request):
        result = {}
        task = []
        # temp = sys.stdout
        schedule = check_alert.scheduler
        f = schedule.get_jobs('default')

        for i in f:
            rule_id = i.id.split('_')[-1]
            check_rule = Rules.objects.filter(id=int(rule_id))
            if len(check_rule) == 1:
                task.append({
                    "id": i.id,
                    "name": check_rule[0].name,
                    "period": check_rule[0].alert_period
                        })
            else:
                task.append({
                    "id": i.id,
                    "name": "not found rule",
                    "period": 0
                        })
        result["results"] = task
        return Response(data=result, status=status.HTTP_200_OK)

    # 删除队列任务
    def delete(self, request, pk):
        result = {}
        task_id = pk
        try:
            schedule = check_alert.scheduler
            f = schedule.get_job(job_id=task_id, jobstore="default")
            if f:
                schedule.remove_job(job_id=task_id, jobstore="default")
            result["code"] = 0
        except Exception as e:
            result["code"] = 1
        return Response(data=result, status=status.HTTP_200_OK)














