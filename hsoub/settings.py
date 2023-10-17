
from pathlib import Path
from django.utils.translation import gettext_lazy as _

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "django-insecure-nw)f3iqlmj-05q5ryjk9(i+hk&*m9a04pekrs_!g0)^rb#e4j0"

DEBUG = True

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "academy",
    "account",
    "checkout",
    "HOD",
    "staff",
    "storages",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    'django.middleware.locale.LocaleMiddleware',
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    'account.LoginCheckMiddleWare.LoginCheckMiddleWare',

]

ROOT_URLCONF = "hsoub.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.i18n",
                "django.contrib.messages.context_processors.messages",
                "academy.custom_context_prosessor.academy_context",
            ],
        },
    },
]

WSGI_APPLICATION = "hsoub.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

USE_L10N = True

LANGUAGES = (
    ('en', _('English')),
    ('ar', _('Arabic')),
)

LOCALE_PATHS = [
    BASE_DIR / 'locale/',
]

STATIC_URL = "static/"
STATIC_ROOT = "/static/"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

MEDIA_URL = "media/"
MEDIA_ROOT = "/media/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "account.User"

AUTHENTICATION_BACKENDS = ['account.EmailBackEnd.EmailBackEnd']


AWS_S3_ACCESS_KEY_ID = "AKIA5ETDILD6N27ZK2FJ" # django
AWS_S3_ACCESS_KEY_ID = "AKIA5ETDILD6AGKN276E"
AWS_S3_SECRET_ACCESS_KEY = "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" # django
AWS_S3_SECRET_ACCESS_KEY = "GUUIAp/ob0u9JGIRoEXwLXN2FlaLoGMIpfOYEJZc"
AWS_STORAGE_BUCKET_NAME = "hsoubacademy"
AWS_S3_FILE_OVERWRITE = False
AWS_S3_VERIFY = True
AWS_LOCATION = 'static'
# AWS_S3_REGION_NAME = "eu-nort"
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

STRIPE_PUBLISHABLE_KEY = "pk_test_51O0QZmIkbWvQwGh2DxLvxByk1uefVmpqTnIVE5yuU2pY6XqAYQCV6arFJcKtzjAdXE63SqsIWytyMwzYy5OS6DMO00NMWpjyvJ"
STRIPE_SECRET_KEY = "sk_test_51O0QZmIkbWvQwGh2LPkRol1xD0k6FCLoRWHTEizVwboO4m1TSwMRa8UzOD95RpIFl87sEiK7Aa1TglvD6p95gmOi00VRsWH9JR"

CURRENCY = "USD"

STRIPE_ENDPOINT_SECRET = "whsec_7d79e148f4c12583a8d151eda6d221f01d2e896a41f3f16cd1d8bad2b5c2a8d0"

