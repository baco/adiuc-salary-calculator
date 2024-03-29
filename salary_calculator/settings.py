# -*- coding: utf-8 -*-

#=============================================
#
# Copyright 2012 David Racca and Matias Molina.
#
# This file is part of ADIUC Salary Calculator.
#
# ADIUC Salary Calculator is free software: you can redistribute it and/or 
# modify it under the terms of the GNU General Public License as published 
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ADIUC Salary Calculator is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ADIUC Salary Calculator.  If not, see 
# <http://www.gnu.org/licenses/>.
#
#=============================================

# Django settings for salary_calculator project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

# True if you want use sqlite3 for local development purposes
DEVEL = True

ADMINS = (
    ('Admin', 'admin@adiuc.org.ar'),
)

MANAGERS = ADMINS

if DEVEL:

	DATABASES = {
		'default': {
		    'ENGINE': 'django.db.backends.sqlite3', 	# Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
		    'NAME': 'salary-calculator.sql',        		# Or path to database file if using sqlite3.
		    'USER': '',                      						# Not used with sqlite3.
		    'PASSWORD': '',      					            # Not used with sqlite3.
		    'HOST': '',                      						# Set to empty string for localhost. Not used with sqlite3.
		    'PORT': '',                      						# Set to empty string for default. Not used with sqlite3.
		}
	}

else:

	DATABASES = {
		'default': {
			'ENGINE': 'django.db.backends.mysql',			# Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
			'NAME': 'mleec_consulta',											# Or path to database file if using sqlite3.
			'USER': 'mleec_consulta',											# Not used with sqlite3.
			'PASSWORD': 'e044c865',									# Not used with sqlite3.
			'HOST': '',											# Set to empty string for localhost. Not used with sqlite3.
			'PORT': '',											# Set to empty string for default. Not used with sqlite3.
		}
	}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Cordoba'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'es-ar'

# Character encoding (UTF-8).
DEFAULT_CHARSET = 'utf-8'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True


MEDIA_ROOT = ''

MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
if DEVEL:
    STATIC_ROOT = ''
else:
    STATIC_ROOT = '/home/mleec/webapps/adiuc_static'


# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
if DEVEL:
    STATIC_URL = '/static/'
else:
    STATIC_URL = 'http://consultas.adiuc.org.ar/static/'


# Additional locations of static files
STATICFILES_DIRS = (
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
if DEVEL:
    SECRET_KEY = 'owu4hx62rtuy!&amp;7w!h&amp;n9k1+92+_p++lfnuhu@%bv&amp;n85nnb9&amp;'
else:
    SECRET_KEY = '5p)g(u+m=4^n&amp;b5c(ef*1i^$sb#ocux@#i+box&amp;zdf(k3@n+ne'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'salary_calculator.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'salary_calculator.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    '/salary_calculator_app/templates',
    '/home/mleec/webapps/adiuc_static/templates'
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    #'django.contrib.sites',
    #'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
     'django.contrib.humanize',
    'salary_calculator_app',
	'django.contrib.staticfiles'
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

DECIMAL_SEPARATOR='.'
