import logging

from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
import django_filters
from django.contrib.auth.models import User
from rulemanager.user.serializers import UserSerializer, UserExpandSerializer
from .models import UserExpand
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Create your views here.


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000


class UserFilter(django_filters.rest_framework.FilterSet):
    class Meta:
        model = User
        fields = ["username", "email"]


class UserExpandFilter(django_filters.rest_framework.FilterSet):
    user__username = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = UserExpand
        fields = ["user__username", "phone", "erp_id"]


class UserViewSet(viewsets.ModelViewSet):
    authentication_classes = (SessionAuthentication, TokenAuthentication,)
    # permission_classes = (IsAuthenticated, )
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    filter_class = UserFilter
    pagination_class = StandardResultsSetPagination


class UserExpandViewSet(viewsets.ModelViewSet):
    authentication_classes = (SessionAuthentication, TokenAuthentication,)
    # permission_classes = (IsAuthenticated, )
    permission_classes = (AllowAny,)
    queryset = UserExpand.objects.all().order_by('-id')
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    filter_class = UserExpandFilter
    serializer_class = UserExpandSerializer
    pagination_class = StandardResultsSetPagination


class AddUser(APIView):
    authentication_classes = (SessionAuthentication, TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)
    permission_classes = (AllowAny,)
    '''
    new
    data = {
    username: '',
    email: '',
    phone: '',
    erp_id: '',
    alert_channel: ''
    }
    update 
    data = {
    id: '',
    username: '',
    email: '',
    phone: '',
    erp_id: '',
    alert_channel: ''
    }
    '''

    def post(self, request):
        data = request.data
        print(data)
        new_user = User.objects.create(username=data['username'], email=data['email'])
        try:
            UserExpand.objects.create(user=new_user, phone=data['phone'], erp_id=data['erp_id'],
                                      alert_channel=data['alert_channel'])
            return Response(status=status.HTTP_200_OK, data={"code": 0})
        except Exception as e:
            logging.error("[-]add new user failed:%s " % e)
            User.delete(new_user)
            return Response(status=status.HTTP_200_OK, data={"code": 1})

    def put(self, request):
        data = request.data
        result = {}
        print(data)
        try:
            update_user = User.objects.get(id=data['user'])
        except Exception as e:
            logging.error("[-] update user failed:%s " % e)
            result['code'] = 1
            return Response(status=status.HTTP_200_OK, data=result)
        # update user email
        update_user.email = data['email']
        update_user.save()
        # update user expand args
        UserExpand.objects.filter(user__id=update_user.pk).update(
            **{"phone": data['phone'], "erp_id": data['erp_id'], "alert_channel": data['alert_channel']})
        result['code'] = 0
        return Response(status=status.HTTP_200_OK, data=result)

    def delete(self, request, pk):
        result = {}
        try:
            user_id = pk
            UserExpand.objects.filter(user__id=user_id).delete()
            User.objects.filter(id=user_id).delete()
            result['code'] = 0
        except Exception as e:
            logging.error("[-] args error,check your input%s" % e)
            result['code'] = 1
        return Response(status=status.HTTP_200_OK, data=result)




