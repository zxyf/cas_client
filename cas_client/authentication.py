# coding: utf-8

'''
author: runforever
'''

from django.core.cache import cache
from django.conf import settings

from rest_framework import exceptions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .utils import IS_PYTHON3

CAS_LOGIN_EXPIRE = getattr(settings, 'CAS_LOGIN_EXPIRE', True)
CAS_LOGIN_EXPIRE_TIME = getattr(settings, 'CAS_LOGIN_EXPIRE_TIME', 7200)
CAS_LOGIN_EXPIRE_KEY = getattr(settings, 'CAS_LOGIN_EXPIRE_KEY', 'LOGIN_USER_')


class ZXAuthentication(JSONWebTokenAuthentication):

    def authenticate(self, request):
        auth_result = super(ZXAuthentication, self).authenticate(request)
        if auth_result is None:
            return None

        user, jwt_value = auth_result

        if CAS_LOGIN_EXPIRE:
            key = 'LOGIN_USER_' + str(user.id)

            token = cache.get(key)
            if token is None:
                raise exceptions.AuthenticationFailed(u'Token 过期，请重新登录')

            if IS_PYTHON3:
                jwt_value = jwt_value.decode('utf-8')
            if token != jwt_value:
                raise exceptions.AuthenticationFailed(u'Token 错误，强制下线')

            cache.set(key, token, CAS_LOGIN_EXPIRE_TIME)
        return (user, jwt_value)
