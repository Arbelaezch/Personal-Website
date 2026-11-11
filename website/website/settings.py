import os
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured
from dotenv import load_dotenv
load_dotenv()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# DJANGO SETTINGS
def _env_bool(name, default=False):
    return os.getenv(name, str(default)).strip().lower() in ('1', 'true', 'yes', 'on')


# Off unless explicitly enabled: put DEBUG=1 in your local .env for development only.
DEBUG = _env_bool('DEBUG', False)

SECRET_KEY = os.getenv('SECRET_KEY')
if not SECRET_KEY:
    raise ImproperlyConfigured('SECRET_KEY is not set (add it to .env, see .env.example)')

# 'DJANGO_ALLOWED_HOSTS' should be a single string of hosts with a space between each.
# For example: 'DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]'
ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', '').split()
if not ALLOWED_HOSTS:
    if DEBUG:
        ALLOWED_HOSTS = ['localhost', '127.0.0.1', '[::1]']
    else:
        raise ImproperlyConfigured('DJANGO_ALLOWED_HOSTS is not set (see .env.example)')


# Application definition

INSTALLED_APPS = [
    # Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party Libraries
    'django_ckeditor_5',
    'rest_framework',
    'corsheaders',
    'django_filters',
    'adminsortable2',

    # Local Apps
    'portfolio',
    'blog',
    'recipes',
    'films',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'website.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
        ],
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

WSGI_APPLICATION = 'website.wsgi.application'


# DATABASE
# DEV_DB_* is used when DEBUG is on, PROD_DB_* otherwise (MySQL in both, for dev/prod parity).
def _database(prefix):
    engine = os.getenv(f'{prefix}_DB_ENGINE')
    if not engine:
        raise ImproperlyConfigured(f'{prefix}_DB_ENGINE is not set (see .env.example)')
    return {
        'ENGINE': engine,
        'HOST': os.getenv(f'{prefix}_DB_HOST', ''),
        'NAME': os.getenv(f'{prefix}_DB_NAME', ''),
        'USER': os.getenv(f'{prefix}_DB_USER', ''),
        'PORT': os.getenv(f'{prefix}_DB_PORT', ''),
        'PASSWORD': os.getenv(f'{prefix}_DB_PASSWORD', ''),
    }


DATABASES = {'default': _database('DEV' if DEBUG else 'PROD')}


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
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/Edmonton'
USE_I18N = True
USE_TZ = True


# STATIC FILES
STATIC_URL = '/static/' # URL to use when referring to static files located in STATIC_ROOT.

# Where django looks for additional static files.
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Where django collects static files.
# Collects them locally; should collect to static bucket for production.
STATIC_ROOT = BASE_DIR / 'staticfiles'


STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# The URL that will serve the media files.
MEDIA_URL = '/media/'
# The directory that will hold the media files.
# The absolute path to the directory that will hold the media files.
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# LOGGING
# Without this, production 500 tracebacks are not logged anywhere (Django only mails admins).
# stderr goes to the journal (journalctl -u gunicorn). django.request is limited to errors (5xx) so
# the bot-scan 404s do not flood the log.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {'console': {'class': 'logging.StreamHandler'}},
    'root': {'handlers': ['console'], 'level': 'WARNING'},
    'loggers': {
        'django.request': {'handlers': ['console'], 'level': 'ERROR', 'propagate': False},
    },
}


# PRODUCTION SECURITY (TLS is terminated by nginx; see deploy/nginx)
if not DEBUG:
    # nginx sets X-Forwarded-Proto (deploy/nginx/snippets/proxy-app.conf)
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    CSRF_TRUSTED_ORIGINS = ['https://christiandonovan.ca', 'https://www.christiandonovan.ca']

SILENCED_SYSTEM_CHECKS = [
    # HSTS is sent by nginx (deploy/nginx/snippets/security-headers.conf); setting it here too
    # would send the header twice.
    'security.W004',
]


CORS_ALLOWED_ORIGINS = [
    "https://christiandonovan.ca",
    "https://www.christiandonovan.ca",
    "https://family-food.vercel.app",  # family-food frontend (Next.js on Vercel)
]
if DEBUG:
    CORS_ALLOWED_ORIGINS += [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000",
    ]

# The public API is read-only.
CORS_ALLOW_METHODS = ["GET", "HEAD", "OPTIONS"]

# The family-food frontend sends credentials: 'include' on its GET requests, and browsers reject the
# response unless this is True. Turn it off once the frontend stops sending credentials (see the
# family-food repo's cleanup issue).
CORS_ALLOW_CREDENTIALS = True
CORS_EXPOSE_HEADERS = ['Content-Type', 'X-CSRFToken']
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    # Anonymous users can read; anything that writes needs a login. New views are safe by default.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
}




# Ckeditor
# RICH-TEXT EDITOR: CKEditor 5 via django-ckeditor-5 (bundled static files, open-source GPL mode).
# The stored content only uses p, ul/ol/li (ol start, li value), br, em, u and sup, so the toolbar is
# small. <li value="..."> is kept via htmlSupport; <ol start="..."> via the list properties.
_LISTS = {'properties': {'startIndex': True, 'reversed': False, 'styles': False}}
_KEEP_LI_VALUE = {'allow': [{'name': 'li', 'attributes': {'value': True}}]}
_BASIC_TOOLBAR = [
    'undo', 'redo', '|',
    'bold', 'italic', 'underline', 'superscript', '|',
    'bulletedList', 'numberedList', '|',
    'removeFormat', 'sourceEditing',
]

CKEDITOR_5_CONFIGS = {
    'default': {'toolbar': _BASIC_TOOLBAR, 'list': _LISTS, 'htmlSupport': _KEEP_LI_VALUE},
    'films': {'toolbar': _BASIC_TOOLBAR, 'list': _LISTS, 'htmlSupport': _KEEP_LI_VALUE},
    # blog.Article.body: headings, links, quotes and images (uploads are staff-only)
    'blog': {
        'toolbar': ['heading', '|'] + _BASIC_TOOLBAR[:-2] + ['|', 'link', 'blockQuote', 'insertImage', '|',
                                                              'removeFormat', 'sourceEditing'],
        'list': _LISTS,
        'htmlSupport': _KEEP_LI_VALUE,
    },
}
CKEDITOR_5_FILE_UPLOAD_PERMISSION = 'staff'
