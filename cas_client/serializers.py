# coding: utf-8

'''
author: runforever
'''

from django.core.cache import cache
from django.conf import settings

from rest_framework_jwt.serializers import JSONWebTokenSerializer


CAS_LOGIN_EXPIRE = getattr(settings, 'CAS_LOGIN_EXPIRE', True)
CAS_LOGIN_EXPIRE_TIME = getattr(settings, 'CAS_LOGIN_EXPIRE_TIME', 7200)
CAS_LOGIN_EXPIRE_KEY = getattr(settings, 'CAS_LOGIN_EXPIRE_KEY', 'LOGIN_USER_')


class ZXJSONWebTokenSerializer(JSONWebTokenSerializer):

    def validate(self, attr):
        auth_data = super(ZXJSONWebTokenSerializer, self).validate(attr)

        if CAS_LOGIN_EXPIRE:
            user = auth_data['user']
            token = auth_data['token']
            key = 'LOGIN_USER_' + str(user.id)
            cache.set(key, token, CAS_LOGIN_EXPIRE_TIME)

        return auth_data
