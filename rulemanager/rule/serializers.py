from rulemanager.rule.models import *
from rest_framework import serializers
from rest_framework_bulk import BulkListSerializer, BulkSerializerMixin


class AlertGroupTUsersSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = AlertGroupTUsers
        list_serializer_class = BulkListSerializer
        fields = "__all__"


class AlertReceivingGroupSerializer(serializers.ModelSerializer):
    alert_user_group = AlertGroupTUsersSerializer(many=True, read_only=True)

    class Meta:
        model = AlertReceivingGroup
        fields = "__all__"


class RuleGroupTAlertGroupSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    group_name = serializers.ReadOnlyField(source='alert_group.name')

    class Meta:
        model = RuleGroupTAlertGroup
        list_serializer_class = BulkListSerializer
        fields = "__all__"


class RuleGroupTAlertUserSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='alert_user.username')

    class Meta:
        model = RuleGroupTAlertUser
        list_serializer_class = BulkListSerializer
        fields = "__all__"


class RuleGroupSerializer(serializers.ModelSerializer):
    alert_groups = RuleGroupTAlertGroupSerializer(many=True, read_only=True)
    alert_users = RuleGroupTAlertUserSerializer(many=True, read_only=True)

    class Meta:
        model = RuleGroup
        fields = "__all__"


class RulesTAlertGroupSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    group_name = serializers.ReadOnlyField(source='alert_group.name')

    class Meta:
        model = RulesTAlertGroup
        list_serializer_class = BulkListSerializer
        fields = "__all__"


class RulesTAlertUsersSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='alert_user.username')

    class Meta:
        model = RulesTAlertUsers
        list_serializer_class = BulkListSerializer
        fields = "__all__"


class RulesSerializer(serializers.ModelSerializer):
    group_name = serializers.ReadOnlyField(source='group.name')
    # 告警接收用户
    rules_users = RulesTAlertUsersSerializer(many=True, read_only=True)
    # 告警接收用户组
    rules_groups = RulesTAlertGroupSerializer(many=True, read_only=True)

    class Meta:
        model = Rules
        fields = "__all__"







