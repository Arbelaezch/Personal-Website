import os
import sys
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# CONF_DIR = os.path.join(BASE_DIR,'..','conf')


# DJANGO SETTINGS
SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = int(os.getenv('DEBUG', default=1))

# 'DJANGO_ALLOWED_HOSTS' should be a single string of hosts with a space between each.
# For example: 'DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]'
ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS").split()

CHECK_AGAIN_MODE = False


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
    'ckeditor',
    'ckeditor_uploader',
    'rest_framework',
    'corsheaders',
    'django_filters',

    # Local Apps
    'portfolio',
    'blog',
    'api',
    'recipes',
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
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': 'db.sqlite3',
#     }
# }

if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': str(os.getenv('DEV_DB_ENGINE')),
            'HOST': str(os.getenv('DEV_DB_HOST')),
            'NAME': str(os.getenv('DEV_DB_NAME')),
            'USER': str(os.getenv('DEV_DB_USER')),
            'PORT': str(os.getenv('DEV_DB_PORT')),
            'PASSWORD': str(os.getenv('DEV_DB_PASSWORD'))
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': str(os.getenv('PROD_DB_ENGINE')),
            'HOST': str(os.getenv('PROD_DB_HOST')),
            'NAME': str(os.getenv('PROD_DB_NAME')),
            'USER': str(os.getenv('PROD_DB_USER')),
            'PORT': str(os.getenv('PROD_DB_PORT')),
            'PASSWORD': str(os.getenv('PROD_DB_PASSWORD'))
        }
    }


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
MEDIA_DIR = 'media/'
# The absolute path to the directory that will hold the media files.
MEDIA_ROOT = os.path.join(BASE_DIR, MEDIA_DIR)


# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'file': {
#             'level': 'DEBUG',
#             'class': 'logging.FileHandler',
#             'filename': '/home/arbelaezch/Personal-Website/website/website/logfile.log',
#         },
#     },
#     'root': {
#         'handlers': ['file'],
#         'level': 'DEBUG',
#     }
# }



CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8000",
    "https://christiandonovan.ca",
    "https://www.christiandonovan.ca",
    "https://family-food.vercel.app",
]

# CORS_ALLOW_ALL_HEADERS = True
CORS_ALLOW_METHODS = [
    "GET",
    "POST",
    "PUT",
    "PATCH",
    "DELETE",
    "OPTIONS",
]

# Allow all cors origins
# CORS_ALLOW_ALL_ORIGINS = True
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
# CORS_ALLOW_METHODS = ['*']
# CORS_ALLOW_HEADERS = ['*']

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    # 'DEFAULT_AUTHENTICATION_CLASSES': [
    #     'rest_framework_simplejwt.authentication.JWTAuthentication',
    # ],
}




# Ckeditor
CKEDITOR_CONFIGS = {
'portal_config': {
    # 'skin': 'moono',
    # 'skin': 'office2013',
    'toolbar_Basic': [
        ['Source', '-', 'Bold', 'Italic']
    ],
    'toolbar_YourCustomToolbarConfig': [
        {'name': 'document', 'items': [
            'Source', '-', 'Save', 'NewPage', 'Preview', 'Print', '-', 'Templates'
        ]},
        {'name': 'clipboard', 'items': [
            'Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo'
        ]},
        {'name': 'editing', 'items': ['Find', 'Replace', '-', 'SelectAll']},
        {'name': 'forms',
         'items': [
             'Form', 'Checkbox', 'Radio', 'TextField', 'Textarea',
             'Select', 'Button', 'ImageButton', 'HiddenField'
         ]},
        '/',
        {'name': 'basicstyles',
         'items': [
             'Bold', 'Italic', 'Underline', 'Strike', 'Subscript',
             'Superscript', '-', 'RemoveFormat'
         ]},
        {'name': 'paragraph',
         'items': [
             'NumberedList', 'BulletedList', '-', 'Outdent', 'Indent',
             '-', 'Blockquote', 'CreateDiv', '-', 'JustifyLeft',
             'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-',
             'BidiLtr', 'BidiRtl', 'Language'
         ]},
        {'name': 'links', 'items': ['Link', 'Unlink', 'Anchor']},
        {'name': 'insert',
         'items': [
             'Image', 'Table', 'HorizontalRule',
             'Smiley', 'SpecialChar', 'PageBreak', 'Iframe'
         ]},
        '/',
        {'name': 'styles', 'items': ['Styles', 'Format', 'Font', 'FontSize']},
        {'name': 'colors', 'items': ['TextColor', 'BGColor']},
        {'name': 'tools', 'items': ['Maximize', 'ShowBlocks']},
        {'name': 'about', 'items': ['About']},
        '/',  # put this to force next toolbar on new line
        {'name': 'yourcustomtools', 'items': [
            # put the name of your editor.ui.addButton here
            'Preview',
            'Maximize',

        ]},
    ],
    'toolbar': 'YourCustomToolbarConfig',  # put selected toolbar config here
    # 'toolbarGroups': [{ 'name': 'document', 'groups': [ 'mode', 'document', 'doctools' ] }],
    # 'height': 291,
    # 'width': '100%',
    # 'filebrowserWindowHeight': 725,
    # 'filebrowserWindowWidth': 940,
    # 'toolbarCanCollapse': True,
    # 'mathJaxLib': '//cdn.mathjax.org/mathjax/2.2-latest/MathJax.js?config=TeX-AMS_HTML',
    'tabSpaces': 4,
    'extraPlugins': ','.join([
        'uploadimage',  # the upload image feature
        # your extra plugins here
        'div',
        'autolink',
        'autoembed',
        'embedsemantic',
        'autogrow',
        # 'devtools',
        'widget',
        'lineutils',
        'clipboard',
        'dialog',
        'dialogui',
        'elementspath'
    ]),
    }
}

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Bold', 'Italic', 'Underline'],
            ['NumberedList', 'BulletedList'],
            ['RemoveFormat']
        ],
        'height': 200,
        'width': '100%',
    }
}

CKEDITOR_UPLOAD_PATH = 'editor_uploads/'