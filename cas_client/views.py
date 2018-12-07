# coding: utf-8

'''
author: runforever
'''

import xmltodict
import requests

from django.utils.module_loading import import_string
from django.conf import settings
from django.core.cache import cache
from django.contrib.auth.models import User
from django.db import transaction

from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.views import JSONWebTokenAPIView

from .utils import get_datetime
from .serializers import ZXJSONWebTokenSerializer

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER

CAS_SERVER_VALIDATE_API = getattr(settings, 'CAS_SERVER_VALIDATE_API', '')
CAS_CLIENT_SERVICE = getattr(settings, 'CAS_CLIENT_SERVICE', '')

CAS_LOGIN_EXPIRE = getattr(settings, 'CAS_LOGIN_EXPIRE', True)
CAS_LOGIN_EXPIRE_TIME = getattr(settings, 'CAS_LOGIN_EXPIRE_TIME', 7200)
CAS_LOGIN_EXPIRE_KEY = getattr(settings, 'CAS_LOGIN_EXPIRE_KEY', 'LOGIN_USER_')


class ClientAuthView(APIView):
    '''
    cas sso client view
    '''

    authentication_classes = ()
    permission_classes = ()

    def get_user(self, user_attributes):
        username = user_attributes['username']
        email = user_attributes['email'] or ''
        is_active = True if user_attributes['is_active'] == "True" else False
        date_joined = get_datetime(user_attributes['date_joined'])
        last_login = get_datetime(user_attributes['last_login'])

        user, _ = User.objects.update_or_create(
            username=username,
            defaults={
                'email': email,
                'is_active': is_active,
                'date_joined': date_joined,
                'last_login': last_login,
            }
        )
        return user

    def auth_user(self, user):
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        auth_info = jwt_response_payload_handler(token, user, self.request)
        return auth_info

    def get(self, request):
        ticket = request.GET.get('ticket', '')
        data = {
            'ticket': ticket,
            'service': CAS_CLIENT_SERVICE,
        }
        namespaces = {
            'http://www.yale.edu/tp/cas': None,
        }

        resp = requests.get(CAS_SERVER_VALIDATE_API, params=data)
        content = resp.content
        resp_dict = xmltodict.parse(
            content,
            process_namespaces=True,
            namespaces=namespaces,
        )
        cas_service_resp = resp_dict['serviceResponse']
        auth_success_info = cas_service_resp.get('authenticationSuccess', {})

        if not auth_success_info:
            return Response(resp_dict, status=400)

        user_attributes = auth_success_info['attributes']
        update_user_profile_method_path = getattr(settings, 'CAS_CILENT_UPDATE_STAFF_METHOD', '')
        update_user_profile_method = import_string(update_user_profile_method_path)

        with transaction.atomic():
            user = self.get_user(user_attributes)
            staff_profile = update_user_profile_method(user, user_attributes)

        auth_info = self.auth_user(user)
        auth_info['username'] = user.username
        auth_info['name'] = staff_profile.name

        if CAS_LOGIN_EXPIRE:
            key = 'LOGIN_USER_' + str(user.id)
            cache.set(key, auth_info['token'], CAS_LOGIN_EXPIRE_TIME)

        return Response(auth_info)


class ZXObtainJSONWebToken(JSONWebTokenAPIView):
    serializer_class = ZXJSONWebTokenSerializer
