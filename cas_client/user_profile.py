# coding: utf-8

'''
author: runforever
'''

from django.utils.module_loading import import_string
from django.conf import settings


def update_user_profile(user, user_attributes):
    phone = user_attributes.get('phone') or ''
    name = user_attributes.get('name') or ''

    staff_model_path = getattr(settings, 'CAS_CLIENT_STAFF_MODEL', '')
    staff_model = import_string(staff_model_path)

    staff_profile, _ = staff_model.objects.update_or_create(
        user_id=user.id,
        defaults={
            'phone': phone,
            'name': name,
        }
    )
    return staff_profile
