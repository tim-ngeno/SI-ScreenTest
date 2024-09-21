import dj_database_url
from os import getenv, path
from dotenv import load_dotenv
from pathlib import Path


load_dotenv()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = getenv("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = getenv("DJANGO_DEBUG", "False").lower() in ("true", "1", "t")
DEBUG = True
ALLOWED_HOSTS = getenv("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "mozilla_django_oidc",
    "rest_framework",
    "api",
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

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

WSGI_APPLICATION = "core.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    "default": dj_database_url.config(
        default=getenv("DATABASE_URL"),
        conn_max_age=600,
        ssl_require=True,
    ),
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = path.join(BASE_DIR, "staticfiles")

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# OIDC CONFIG
OKTA_DOMAIN = getenv("OKTA_DOMAIN")
OIDC_RP_CLIENT_ID = getenv("OIDC_CLIENT_ID")
OIDC_RP_CLIENT_SECRET = getenv("OIDC_CLIENT_SECRET")
OIDC_OP_AUTHORIZATION_ENDPOINT = f"https://{OKTA_DOMAIN}/oauth2/default/v1/authorize"
OIDC_OP_USER_ENDPOINT = f"https://{OKTA_DOMAIN}/oauth2/default/v1/userinfo"
OIDC_OP_TOKEN_ENDPOINT = f"https://{OKTA_DOMAIN}/oauth2/default/v1/token"
OIDC_OP_JWKS_ENDPOINT = f"https://{OKTA_DOMAIN}/oauth2/default/v1/keys"


# Handle storing and refresh of tokens

AUTHENTICATION_BACKENDS = (
    "core.backends.CustomOIDCAuthenticationBackend",
    "django.contrib.auth.backends.ModelBackend",
)

OIDC_RENEW_ID_TOKEN_EXPIRY_SECONDS = 60 * 60
OIDC_STORE_ACCESS_TOKEN = getenv("OIDC_STORE_ACCESS_TOKEN", True)
OIDC_STORE_ID_TOKEN = getenv("OIDC_STORE_ID_TOKEN", True)
OIDC_STORE_REFRESH_TOKEN = getenv("OIDC_STORE_REFRESH_TOKEN", True)
OIDC_RP_SCOPES = getenv("OIDC_RP_SCOPES", "openid profile email offline_access")


# Use state and access tokens for session management
OIDC_USE_STATE = True
OIDC_STORE_ID_TOKEN = True
OIDC_STORE_ACCESS_TOKEN = True

OIDC_RP_SIGN_ALGO = "RS256"

# Map user information returned from Okta to django user attributes
OIDC_CREATE_USER = True
OIDC_EXEMPT_URLS = ["oidc/callback/"]


LOGIN_URL = "/oidc/authenticate/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"
