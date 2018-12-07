# coding: utf-8

'''
author: runforever
'''

from django.contrib.auth.backends import ModelBackend
from django.core.cache import cache
from django.conf import settings

CAS_LOGIN_EXPIRE_TIME = getattr(settings, 'CAS_LOGIN_EXPIRE_TIME', 7200)
CAS_LOGIN_EXPIRE_KEY = getattr(settings, 'CAS_LOGIN_EXPIRE_KEY', 'LOGIN_USER_')


class ZXAuthBackend(ModelBackend):

    def authenticate(self, username=None, password=None, **kwargs):
        user = super(ZXAuthBackend, self).authenticate(username, password, **kwargs)
        if user:
            key = 'LOGIN_USER_' + str(user.id)
            cache.set(key, 1, CAS_LOGIN_EXPIRE_TIME)
        return user
