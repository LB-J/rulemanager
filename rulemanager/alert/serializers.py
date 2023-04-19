from rulemanager.alert.models import *
from rest_framework import serializers
from rest_framework_bulk import BulkListSerializer, BulkSerializerMixin


class SendRecordsSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='alert_user.username')

    class Meta:
        model = SendRecords
        fields = "__all__"


class AckRecordsSerializer(serializers.ModelSerializer):

    class Meta:
        model = AckRecords
        fields = "__all__"


class AlertRecordsSerializer(serializers.ModelSerializer):
    alert_ack = AckRecordsSerializer(many=True, read_only=True)
    alert_send = SendRecordsSerializer(many=True, read_only=True)

    class Meta:
        model = AlertRecords
        fields = "__all__"




