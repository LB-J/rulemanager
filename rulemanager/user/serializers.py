from django.contrib.auth.models import User, Group, Permission
from rest_framework import serializers
from .models import UserExpand


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("id", 'username', 'email', "first_name", "last_name")


class UserExpandSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')
    email = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = UserExpand
        fields = ("id", "user", 'username', "phone", "erp_id", "email", "alert_channel")

