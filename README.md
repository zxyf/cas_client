#  SSO 接入 Client

## 依赖
1. Django>=1.9.10
2. djangorestframework>=3.5.3
3. xmltodict
4. djangorestframework-jwt

## 安装
使用 pip 安装

```
pip install git+https://github.com/zxyf/cas_client.git
```

添加requirements.txt
```
git+http://github.com/zxyf/cas_client.git
```

## 配置

```
# django install app

INSTALLED_APPS += ['cas_client']

# add SSO settings
# SSO 认证地址
CAS_SERVER_VALIDATE_API = 'http://xxx.com/cas/p3/serviceValidate/'
# SSO 登录地址
CAS_SERVER_LOGIN_URL = 'http://xxx.com/cas/login/'
# SSO client 认证
CAS_CLIENT_SERVICE = 'http://www.yourclient.com/cas/auth/'

# 未登录跳转
LOGIN_URL = '{0}?service={1}'.format(CAS_SERVER_LOGIN_URL, CAS_CLIENT_SERVICE )

# CAS CLIENT
# 用户模型
CAS_CLIENT_STAFF_MODEL = 'xxx.models.StaffProfile'

# 更新用户模型方法
CAS_CILENT_UPDATE_STAFF_METHOD = 'cas_client.user_profile.update_user_profile'

# urls.py 添加 url
urlpatterns += [url(r'^cas/', include('cas_client.urls'))]
```

### 两小时不操作超时配置
`settings.py` 配置
```
# 开启不操作 token 过期
CAS_LOGIN_EXPIRE = True

# 两小时不操作超时
CAS_LOGIN_EXPIRE_TIME = 7200

# 缓存 key 前缀
CAS_LOGIN_EXPIRE_KEY = 'LOGIN_USER_'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'cas_client.authentication.ZXAuthentication',
    ),
}
```

`urls.py` 登录配置（开发调试时使用）
```
from cas_client.views import ZXObtainJSONWebToken

urlpatterns = [
    url(r'^login/', ZXObtainJSONWebToken.as_view()),
]
```
*注意：需要配置 Django 缓存*
