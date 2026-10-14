import os
from pathlib import Path
import dj_database_url
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-only-change-this-before-production")
DEBUG = os.environ.get("DEBUG", "False").lower() == "true"
ALLOWED_HOSTS = [x.strip() for x in os.environ.get("ALLOWED_HOSTS", ".onrender.com,localhost,127.0.0.1").split(",") if x.strip()]
CSRF_TRUSTED_ORIGINS = [x.strip() for x in os.environ.get("CSRF_TRUSTED_ORIGINS", "https://*.onrender.com").split(",") if x.strip()]
INSTALLED_APPS = ["django.contrib.admin", "django.contrib.auth", "django.contrib.contenttypes", "django.contrib.sessions", "django.contrib.messages", "django.contrib.staticfiles", "analyzer"]
MIDDLEWARE = ["django.middleware.security.SecurityMiddleware", "whitenoise.middleware.WhiteNoiseMiddleware", "django.contrib.sessions.middleware.SessionMiddleware", "django.middleware.common.CommonMiddleware", "django.middleware.csrf.CsrfViewMiddleware", "django.contrib.auth.middleware.AuthenticationMiddleware", "django.contrib.messages.middleware.MessageMiddleware", "django.middleware.clickjacking.XFrameOptionsMiddleware"]
ROOT_URLCONF = "cbsite.urls"
TEMPLATES = [{"BACKEND":"django.template.backends.django.DjangoTemplates","DIRS":[BASE_DIR / "templates"],"APP_DIRS":True,"OPTIONS":{"context_processors":["django.template.context_processors.request","django.contrib.auth.context_processors.auth","django.contrib.messages.context_processors.messages"]}}]
WSGI_APPLICATION = "cbsite.wsgi.application"
DATABASES = {"default": dj_database_url.config(default=os.environ.get("DATABASE_URL", "sqlite:///db.sqlite3"), conn_max_age=600, ssl_require=not DEBUG and os.environ.get("DATABASE_URL", "").startswith("postgres"))}
AUTH_PASSWORD_VALIDATORS = [{"NAME":"django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},{"NAME":"django.contrib.auth.password_validation.MinimumLengthValidator"},{"NAME":"django.contrib.auth.password_validation.CommonPasswordValidator"},{"NAME":"django.contrib.auth.password_validation.NumericPasswordValidator"}]
LANGUAGE_CODE = "ar"
TIME_ZONE = "Asia/Aden"
USE_I18N = True
USE_TZ = True
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_HTTPONLY = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
