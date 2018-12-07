from setuptools import setup

PACKAGE = "cas_client"
NAME = "CAS Client"
DESCRIPTION = "CAS Client"
AUTHOR = "runforever"
AUTHOR_EMAIL = "c.chenchao.c@gmail.com"
URL = "blog.defcoding.com"
VERSION = '1.0.0'

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license="BSD",
    url=URL,
    packages=[PACKAGE],
    install_requires=[
        'django',
        'requests',
        'xmltodict',
        'djangorestframework',
        'djangorestframework-jwt',
    ],
    zip_safe=False,
)
