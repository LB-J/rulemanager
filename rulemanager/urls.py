"""rulemanager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework_bulk.routes import BulkRouter
from django.conf.urls import include
from django.urls import re_path as url
from rulemanager import settings
from django.conf.urls.static import static
from rulemanager.rule import views as rule_view
from rulemanager.alert import views as alert_view
from rulemanager.user import views as user_view
from django.views.generic import TemplateView

bulk_router = BulkRouter()
bulk_router.register(r'rule/alert_group', rule_view.AlertReceivingGroupViewSet)
bulk_router.register(r'rule/alter_user', rule_view.AlertGroupTUsersViewSet)
bulk_router.register(r'rule/rule_group', rule_view.RuleGroupViewSet)
bulk_router.register(r'rule/group/rule_alert/group', rule_view.RuleGroupTAlertGroupViewSet)
# bulk_router.register(r'rule/group/rule_alert/users', rule_view.RuleGroupTAlertUserViewSet)
bulk_router.register(r'rule/common/rules', rule_view.RulesViewSet)
# 2023-05-12 弃用
# bulk_router.register(r'rule/relation/rules_alert/group', rule_view.RulesTAlertGroupViewSet)
bulk_router.register(r'rule/relation/rules_alert/users', rule_view.RulesTAlertUsersViewSet)
bulk_router.register(r'alert/alert_records', alert_view.AlertRecordsViewSet)
bulk_router.register(r'alert/ack_records', alert_view.AckRecordsViewSet)
bulk_router.register(r'alert/send_records', alert_view.SendRecordsViewSet)
bulk_router.register(r'user/detail', user_view.UserViewSet)
bulk_router.register(r'user/expand', user_view.UserExpandViewSet)


urlpatterns = [
    url(r'^rulemanager/api/', include(bulk_router.urls)),
    path('rulemanager/admin/', admin.site.urls),
    url(r'^$', TemplateView.as_view(template_name="index.html")),
    url(r'^rulemanager/$', TemplateView.as_view(template_name="index.html")),
    # alert web hook
    url(r'^rulemanager/api/web_hook/', alert_view.WebHook.as_view()),
    # add new user
    url(r'^rulemanager/api/user/add/$', user_view.AddUser.as_view()),
    url(r'^rulemanager/api/user/add/(?P<pk>[^/.]+)/$', user_view.AddUser.as_view()),

    # add new user group
    url(r'^rulemanager/api/group/edit/$', alert_view.AddGroup.as_view()),
    url(r'^rulemanager/api/group/edit/(?P<pk>[^/.]+)/$', alert_view.AddGroup.as_view()),
    # ack alert
    url(r'^rulemanager/api/alert_ack/$', alert_view.AckAlert.as_view()),

    # edit new rule group ==> alert group
    url(r'^rulemanager/api/rule_group/edit/$', rule_view.RuleGroupAdd.as_view()),
    url(r'^rulemanager/api/rule_group/edit/(?P<pk>[^/.]+)/$', rule_view.RuleGroupAdd.as_view()),
    # get task SchedulerTask
    url(r'^rulemanager/api/scheduler/task/$', alert_view.SchedulerTask.as_view()),
    url(r'^rulemanager/api/scheduler/task/(?P<pk>[^/.]+)/$', alert_view.SchedulerTask.as_view()),

    # edit  rule  ==> alert user
    url(r'^rulemanager/api/rule/edit/$', rule_view.RuleUserAdd.as_view()),
    # update rule status
    url(r'^rulemanager/api/rule/status/$', rule_view.UpdateRuleStatus.as_view()),
    # generate default alert
    url(r'^rulemanager/api/rule/import/$', rule_view.AutoDefaultAlert.as_view()),
    # login
    path('rulemanager/api/auth/', include('dj_rest_auth.urls')),
    url(r'^rulemanager/login/auth/', include('djoser.urls')),
    url(r'^rulemanager/login/auth/', include('djoser.urls.jwt')),

] + static(settings.STATIC_URL, document_root=settings.STATICS_DIR)

