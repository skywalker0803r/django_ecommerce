"""
Django settings for ecommerce_project project.

Generated by 'django-admin startproject' using Django 5.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-7%utz6#opxo5cig7ph&sqxlkg3w%sm3^72)+ow#4d#6*^^m8)@"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = ['django-ecommerce-kt79.onrender.com', 'localhost','127.0.0.1']



# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'ecommerce',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "ecommerce_project.urls"

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
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "ecommerce_project.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/
# 静态文件 URL，用于浏览器访问
STATIC_URL = '/static/'

# 静态文件存储路径（用于生产环境）
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # 推荐将静态文件放到 `staticfiles` 目录

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'ecommerce/static'),
]

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# 媒體文件配置
MEDIA_URL = '/media/'  # 媒體文件的 URL 路徑
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # 媒體文件的儲存根目錄

# 設置登入後跳轉的頁面
LOGIN_REDIRECT_URL = '/profile/'

# 設置登出後跳轉的頁面
LOGOUT_REDIRECT_URL = '/'

# PayPal 配置
PAYPAL_CLIENT_ID = 'AUyu6u-V30cYsBHn73O9NmM9NGxQ9zVi_4tyLnyr7c_yb1AMtSRTNHFwyGV3zMRvylHNhEj-QlisRzmS'
PAYPAL_CLIENT_SECRET = 'ENWvCuduaXsCgXuhK5CkL21zZnSjCmlIjlLcKeJSJ6eqibpzY7OGThiINqb7paAjSdHOx9HsaWHxh5uJ'
PAYPAL_MODE = 'sandbox'  # 'live' 為正式環境

