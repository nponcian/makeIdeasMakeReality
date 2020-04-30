"""
Django settings for makeIdeasMakeReality project.

Generated by 'django-admin startproject' using Django 3.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['MIMR_SETTINGS_SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ['MIMR_SETTINGS_DEBUG'] == "True"

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'home',
    'service',
    'text',
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

ROOT_URLCONF = 'makeIdeasMakeReality.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'makeIdeasMakeReality.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['MIMR_SETTINGS_DB_NAME'],
        'USER': os.environ['MIMR_SETTINGS_DB_USER'],
        'PASSWORD': os.environ['MIMR_SETTINGS_DB_PASSWORD'],
        'HOST': os.environ['MIMR_SETTINGS_DB_HOST'],
        'PORT': os.environ['MIMR_SETTINGS_DB_PORT'],
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

if os.environ['MIMR_SETTINGS_IS_DEVELOPMENT'] == "True": # For development
    STATIC_URL = '/static/'
    # The base url to access the static files
    # "static" word could be anything, but it is the standard name
    # URL to use when referring to static files located in STATIC_ROOT.
    # If this STATIC_URL is used as a tag in the HTML
    #     {% load static %}
    #     <img src="{% static 'home/assets/img/homeJumbotron.jpg' %}">
    # The loaded "static" tag is substituted to the value of the "STATIC_URL"
    #     <img src="/static/home/assets/img/homeJumbotron.jpg">
    # Since it is not a full link, then it will just be accessed on the current server
    #     http://35.192.166.203:8003/static/home/assets/img/homeJumbotron.jpg
    #  So, such HTTP GET request would again reach the current server. Then, if nginx is configured
    #  to catch URLs with the STATIC_URL prefix
    #      location /static/ { alias /var/www/makeIdeasMakeReality/; }
    #  Thus, the prefix "/static/" as configured in nginx would be replaced with the alias value
    #  of "/var/www/makeIdeasMakeReality/", leading to the file in the local server
    #      /var/www/makeIdeasMakeReality/home/assets/img/homeJumbotron.jpg
else: # For production
    # Method 1 (easier, manual copying of all static files for every change)
    #     1. Create a new bucket in Google Cloud Storage
    #     2. Run collectstatic and either manually copy (upload) the files from the STATIC_ROOT to
    #        the GCS bucket or use tools such as gsutil rsync
    #     3. STATIC_URL = 'https://storage.googleapis.com/mimr-bucket/'
    #     4. Those accesing any static files in the GCS should either be prefixed with this STATIC_URL
    #        through the {% load static %} or directly have the complete URL of the target resource in GCS
    # Method 2 (harder, automatic handling of static files to target storage)
    # NOTE: This effectively disregards STATIC_ROOT as all static files present in all STATICFILES_DIRS
    #       would now go directly to the target storage (so collectstatic would store files directly
    #       to Google Cloud, without anymore filling up /var/www/makeIdeasMakeReality/)
    # 1. Create a new bucket in Google Cloud Storage
    # 2. Change the current Default: 'django.core.files.storage.FileSystemStorage'
    # Default file storage class to be used for any file-related operations that don’t specify a
    # particular storage system.
    # Set the default storage and bucket name in your settings.py file:
    # from django.core.files.storage import default_storage
    # from storages.backends.gcloud import GoogleCloudStorage
    DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage' # print(default_storage.__class__)
    GS_BUCKET_NAME = 'mimr-bucket'
    # 3. Change the current Default: 'django.contrib.staticfiles.storage.StaticFilesStorage'
    # The file storage engine to use when collecting static files with the collectstatic management command.
    # To allow django-admin.py collectstatic to automatically put your static files in your bucket set
    # the following in your settings.py:
    STATICFILES_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
    # 4. The base url
    # See notes For development above
    # For public access, instead of prefixing with
    #     https://storage.cloud.google.com/ # this would require users to log-in their Google account
    # Use
    #     https://storage.googleapis.com/
    STATIC_URL = 'https://storage.googleapis.com/{}/'.format(GS_BUCKET_NAME)
    # 5. Create an IAM Service Account with permission to access the Cloud Storage (e.g. Project
    #    Owner) and generate a JSON key from it.
    # 6. either export environment variable GOOGLE_APPLICATION_CREDENTIALS or define GS_CREDENTIALS
    # export GOOGLE_APPLICATION_CREDENTIALS="/home/user/Downloads/[FILE_NAME].json"
    # from google.oauth2 import service_account
    # GS_CREDENTIALS = service_account.Credentials.from_service_account_file(
    #     "path/to/credentials.json"
    # )

# The absolute path to the directory where collectstatic will collect static files for deployment.
# The location in the local directory of the server serving static files to where the static files
# are stored. This is used for ease of deployment as ALL static files used by the project would be
# in a single location only.
# ex.
#     /var/www/makeIdeasMakeReality/
# Thus, based on the above URL, the file should be located in:
#     /var/www/makeIdeasMakeReality/home/assets/img/homeJumbotron.jpg
# Runnng collectstatic would copy (not move) all files and subdirectories coming from the paths in
# STATICFILES_DIRS and places them to a single location which is this STATIC_ROOT. So it
# important to note that if this path is outside the /home/user/, then it might be needed to run
# collectstatic as sudo to have write access to paths such as /var/www/
STATIC_ROOT = os.environ['MIMR_SETTINGS_STATIC_ROOT']

# The locations in the local directory to where the different static files to be served are located.
# 1. If running with manage.py-runserver (with DEBUG=True and django.contrib.staticfiles), then these
#    locations are automatically functional to serve the static files inside them.
# 2. If running with Gunicorn or Nginx, these locations aren't automatically searched. The Nginx
#    server should be informed first about the location to where the static files are. This is only 1
#    location, which is the one indicated in STATIC_ROOT, such as /var/www/makeIdeasMakeReality/. Now
#    we have a single location to where every static file should come from. Next is we should put all
#    current static files that are possibly located in multiple locations (the locations indicated in
#    STATICFILES_DIRS) to the target single location by running <./manage.py collectstatic>. As the
#    name suggests, what it does is put all the files and directories located in each of the
#    STATICFILES_DIRS and copy them (not move) to the STATIC_ROOT location, ready to be served by
#    Nginx (if configured to read from the location stated in STATIC_ROOT).
STATICFILES_DIRS = [
    # os.path.join(BASE_DIR, "static"),
    os.path.join(BASE_DIR, 'templates'),
    os.path.join(BASE_DIR, "home", "templates"),
    os.path.join(BASE_DIR, "service", "templates"),
    os.path.join(BASE_DIR, "text", "templates"),
]
