import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEBUG = False

DATABASES = {
    'default': {
       'ENGINE': 'dj_db_conn_pool.backends.mysql',
       'NAME': 'rulemanager',
       'HOST': 'mysqldb',
       'USER': 'root',
       'PORT': 3306,
       'PASSWORD': 'my-secret-Pw03',
       'POOL_OPTIONS': {
            'POOL_SIZE': 10,
            'MAX_OVERFLOW': -1,
            'RECYCLE': 28800
        }
    }
}

#  ap schedule task
ap_redis_host = "redisdb"
ap_redis_port = 31010
ap_redis_password = "ub0NEn9Oc8gQoism"
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://%s:%s/3" % (ap_redis_host, ap_redis_port),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {"max_connections": 10},
            "PASSWORD": ap_redis_password,
        }
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {asctime} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'formatter': 'simple',
            'filename': '/data/server/logs/debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

# mail 用于发送告警邮件
SMTP_MAIL = ""
USER_MAIL = ""
PASSWORD_MAIL = ""
# 企业微信接口配置，请从企业微信后台创建应用，获取
# 企业ID
wx_corp_id = ""
# 运维告警平台
wx_corp_secret = "N"
# 应用ID
wx_agent_id = 10000
