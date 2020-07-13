"""
Django settings for django_fund_web project.

Generated by 'django-admin startproject' using Django 1.11.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '8&)pym--3j=)jji9-zl734bt-6&it4outja%+gg*-r694&)951'
SECRET_SALT = "asdqwe"
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'system','index',
    'user',
    'article',
    'filter',
    'payment',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'django_fund_web.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,"templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'django_fund_web.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'fund_web',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': '127.0.0.1',
        'PORT': '3306'

    }
}

# 打印日志，用于测试models
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'console':{
#             'level':'DEBUG',
#             'class':'logging.StreamHandler',
#         },
#     },
#     'loggers': {
#         'django.db.backends': {
#             'handlers': ['console'],
#             'propagate': True,
#             'level':'DEBUG',
#         },
#     }
# }

## celery占用了redis 10库
CACHES = {
    "default":{
        "BACKEND":"django_redis.cache.RedisCache",
        "LOCATION":"redis://127.0.0.1:6379/13",
        "OPTIONS":{
            "CLIENT_CLASS":"django_redis.client.DefaultClient"
        }
    },
    "django_session":{
        "BACKEND":"django_redis.cache.RedisCache",
        "LOCATION":"redis://127.0.0.1:6379/12",
        "OPTIONS":{
            "CLIENT_CLASS":"django_redis.client.DefaultClient"
        }
    },
    "project_dict":{
        "BACKEND":"django_redis.cache.RedisCache",
        "LOCATION":"redis://127.0.0.1:6379/11",
        "OPTIONS":{
            "CLIENT_CLASS":"django_redis.client.DefaultClient"
        }
    },
    "likes":{
        "BACKEND":"django_redis.cache.RedisCache",
        "LOCATION":"redis://127.0.0.1:6379/14",
        "OPTIONS":{
            "CLIENT_CLASS":"django_redis.client.DefaultClient"
        }
    },
}

# 定义一个cache(本地缓存来存储信息,cahe指定的是redis
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
# 指定本地的session使用的本地缓存名称是'default
SESSION_CACHE_ALIAS = "django_session"

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True




# 发送邮件地址
EMAIL_BACKED = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.qq.com'
EMAIL_PORT = 25
EMAIL_HOST_USER = 'nickZlbzy@qq.com'
EMAIL_HOST_PASSWORD = 'ovvjhhcyyiptbhdf'
EMAIL_USE_TLS = False #向服务器通信时，是否启动TLS连接（安全连接） 默认Flase 实际开发设置成True



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

#静态文件目录配置
STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)

#alipay - keyfile
ALIPAY_KEY_DIRS = os.path.join(BASE_DIR,"static/pay/key_file/")

# 保存一天登陆状态
SESSION_COOKIE_AGE = 60*60*24

# 静态资源配置
STATIC_ROOT = '/Users/nick/PycharmProjects/fProject/fund_static/static'

