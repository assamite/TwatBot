"""
Django settings for TwatBot project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""
import lsettings as ls

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
ROOT_DIR = os.path.join(BASE_DIR, '..')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ls.SECRET_KEY

# Twitter API keys
TWITTER_API_KEY = ls.TWITTER_API_KEY or ''
TWITTER_API_SECRET = ls.TWITTER_API_SECRET or ''
TWITTER_ACCESS_TOKEN = ls.TWITTER_ACCESS_TOKEN or ''
TWITTER_ACCESS_TOKEN_SECRET = ls.TWITTER_ACCESS_TOKEN_SECRET or ''

FLICKR_API_KEY = ls.FLICKR_API_KEY
FLICKR_API_SECRET = ls.FLICKR_API_SECRET

UCLASSIFY_API_READ = ls.UCLASSIFY_API_READ or ''
UCLASSIFY_API_WRITE = ls.UCLASSIFY_API_WRITE or ''

WORD2VEC_MODEL_PATH = '/Users/pihatonttu/nltk_data/gensim/googlenews_gensim_v2w.model'
WORD2VEC_MODEL = None
if len(WORD2VEC_MODEL_PATH) > 0:
    import gensim
    WORD2VEC_MODEL = gensim.models.Word2Vec.load(WORD2VEC_MODEL_PATH)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'django.core.context_processors.csrf',
    'django.contrib.messages.context_processors.messages',
)

TEMPLATE_DIRS = template_dirs = ( 
    os.path.join(ROOT_DIR, 'tweets', 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'south',
    'django_cron',
    'tweets'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'TwatBot.urls'

WSGI_APPLICATION = 'TwatBot.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': ls.DATABASE,
        'USER': ls.DB_USER,
        'PASSWORD': ls.DB_PASSWORD,
        'DEFAULT_CHARSET': 'utf-8',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Helsinki'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

CRON_CLASSES = [
    "tweets.cron.TwitterAccountListener",
    "tweets.cron.NewAgeTweeter",
    "tweets.cron.HomeTimelineCleaner"
]

ORIGINAL_IMAGE_UPLOAD_PATH = os.path.join('images', 'original')
PROCESSED_IMAGE_UPLOAD_PATH = os.path.join('images', 'processed')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'default': {
            'format': '%(asctime)s %(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        },           
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'debug.log'),
            'formatter': 'default',
        },
        'cron': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'django_cron.log'),
            'formatter': 'default',
        },
                 
        'default': {
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'tweets_default.log'),
            'formatter': 'default'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.cron': {
            'handlers': ['cron', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'tweets.core': {
            'handlers': ['default', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'tweets.default': {
            'handlers': ['default', 'console'],
            'level': 'DEBUG',
            'propagate': False,
        }
    },    
}
