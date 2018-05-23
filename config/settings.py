from datetime import timedelta

from celery.schedules import crontab


DEBUG = True
LOG_LEVEL = 'DEBUG'  # CRITICAL / ERROR / WARNING / INFO / DEBUG
DEBUG_TB_INTERCEPT_REDIRECTS = False
APP_ROOT = '../hms'

SERVER_TYPE = 'local'
SERVER_NAME = 'www.local_alphanets.ai'
WTF_CSRF_ENABLED = False
SECRET_KEY = 'insecurekeyfordev'

# Flask-Mail.
# MAIL_DEFAULT_SENDER = ''
# MAIL_SERVER = ''
MAIL_DEFAULT_SENDER = 'alpha.analytics.cop@local.host'
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USE_SSL = False
# MAIL_USERNAME = 'you@gmail.com'
# MAIL_PASSWORD = 'awesomepassword'
MAIL_USERNAME = 'alpha.analytics.cop@gmail.com'
MAIL_PASSWORD = 'alpha2018'

# Flask-Babel.
LANGUAGES = {
    'en': 'English',
    # 'kl': 'Klingon',
    # 'es': 'Spanish'
}
BABEL_DEFAULT_LOCALE = 'en'

# asset
WEBPACK_MANIFEST_PATH = APP_ROOT + '/build/manifest.json'

# Celery.
CELERY_BROKER_URL = 'redis://:devpassword@redis:6379/0'
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_REDIS_MAX_CONNECTIONS = 5
CELERYBEAT_SCHEDULE = {
    'mark-soon-to-expire-credit-cards': {
        'task': 'hms.blueprints.billing.tasks.mark_old_credit_cards',
        'schedule': crontab(hour=0, minute=0)
    },
    # 'expire-old-coupons': {
    #     'task': 'hms.blueprints.billing.tasks.expire_old_coupons',
    #     'schedule': crontab(hour=0, minute=1)
    # },
}

# SQLAlchemy.
db_uri = 'postgresql://spark:alpha2018@183.111.230.254:5432/hms'
# db_uri = 'postgresql://spark:1234567@192.168.0.62:5432/hms'
# db_uri = 'postgresql://spark:1234567@192.168.0.61:5432/hms'

# db_uri = 'postgresql://spark:alpha2017@alphadb.c4jyep4rijvc.ap-northeast-2.rds.amazonaws.com:5432/hms'
SQLALCHEMY_DATABASE_URI = db_uri
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_BINDS = {
    'gisdb': 'postgresql://spark:alpha2018@183.111.230.254:5432/gisdb',
    'hms_user': 'postgresql://spark:alpha2018@183.111.230.254:5432/hms_user',
    'hms_system': 'postgresql://spark:alpha2018@183.111.230.254:5432/hms_system',
    'hms': 'postgresql://spark:alpha2018@183.111.230.254:5432/hms'
    # 'gisdb': 'postgresql://spark:1234567@192.168.0.62:5432/gisdb'
    # 'gisdb': 'postgresql://spark:1234567@192.168.0.61:5432/gisdb'
    # 'gisdb': 'postgresql://spark:alpha2017@alphadb.c4jyep4rijvc.ap-northeast-2.rds.amazonaws.com:5432/gisdb'
}

# cache
CACHE_TYPE = 'redis'
CACHE_REDIS_URL = 'redis://localhost:6370/0'
# CACHE_KEY_PREFIX = APP_NAME

# User.
SEED_ADMIN_EMAIL = 'dev@local.host'
SEED_ADMIN_PASSWORD = 'devpassword'
REMEMBER_COOKIE_DURATION = timedelta(days=90)

# Billing.
STRIPE_SECRET_KEY = None
STRIPE_PUBLISHABLE_KEY = None
STRIPE_API_VERSION = '2016-03-07'
STRIPE_CURRENCY = 'usd'
STRIPE_PLANS = {
    '0': {
        'id': 'bronze',
        'name': 'Bronze',
        'amount': 100,
        'currency': STRIPE_CURRENCY,
        'interval': 'month',
        'interval_count': 1,
        'trial_period_days': 14,
        'statement_descriptor': 'hms BRONZE',
        'metadata': {
            'coins': 110
        }
    },
    '1': {
        'id': 'gold',
        'name': 'Gold',
        'amount': 500,
        'currency': STRIPE_CURRENCY,
        'interval': 'month',
        'interval_count': 1,
        'trial_period_days': 14,
        'statement_descriptor': 'hms GOLD',
        'metadata': {
            'coins': 600,
            'recommended': True
        }
    },
    '2': {
        'id': 'platinum',
        'name': 'Platinum',
        'amount': 1000,
        'currency': STRIPE_CURRENCY,
        'interval': 'month',
        'interval_count': 1,
        'trial_period_days': 14,
        'statement_descriptor': 'hms PLATINUM',
        'metadata': {
            'coins': 1500
        }
    }
}

COIN_BUNDLES = [
    {'coins': 100, 'price_in_cents': 100, 'label': '100 for $1'},
    {'coins': 1000, 'price_in_cents': 900, 'label': '1,000 for $9'},
    {'coins': 5000, 'price_in_cents': 4000, 'label': '5,000 for $40'},
    {'coins': 10000, 'price_in_cents': 7000, 'label': '10,000 for $70'},
]

# Bet.
DICE_ROLL_PAYOUT = {
    '2': 36.0,
    '3': 18.0,
    '4': 12.0,
    '5': 9.0,
    '6': 7.2,
    '7': 6.0,
    '8': 7.2,
    '9': 9.0,
    '10': 12.0,
    '11': 18.0,
    '12': 36.0
}

RATELIMIT_STORAGE_URL = CELERY_BROKER_URL
RATELIMIT_STRATEGY = 'fixed-window-elastic-expiry'
RATELIMIT_HEADERS_ENABLED = True

# REST API Connection Info

if SERVER_TYPE is 'local':
    VWORLD_API_KEY = 'A2D7B074-4BE3-3253-BA1B-04619AC46675'
else:
    VWORLD_API_KEY = '483E0418-2F46-3223-80A1-F66D16A24685'

LIVY_URL = 'http://183.111.230.251:8998/'
HDFS_URL = 'hdfs://183.111.230.251:9000/'

## statistic board
NOORI_API_KEY = "dc0c6371a661434fa456c8b23ad1b9ce"
NOORI_URL = "http://stat.molit.go.kr/portal/openapi/service/rest/getList.do"

KOSIS_API_KEY = "MjBhMmY2ZjUzOTMwMzkyYmQ3ZWNjMzEzMzJlMmVkNmY="
KOSIS_URL = "http://kosis.kr/openapi/statisticsData.do?method=getList"

ECOS_API_KEY = "Z0BPT8N98YA1QSGZ2A7N"
ECOS_URL = "http://ecos.bok.or.kr/api/"
