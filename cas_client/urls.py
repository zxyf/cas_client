# coding: utf-8

'''
author: runforever
'''

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^auth/$', views.ClientAuthView.as_view()),
]
