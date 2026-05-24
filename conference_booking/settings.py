from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# ====================
# 🔐 SECURITY WARNING
# ====================
SECRET_KEY = 'django-insecure-8x9y7z6w5v4u3t2s1r0q9p8o7n6m5l4k3j2i1h0g9f8e7d6c5b4a3'
DEBUG = False
ALLOWED_HOSTS = ['.onrender.com', 'localhost', '127.0.0.1', 'bantondos.onrender.com']
SITE_URL = 'https://bantondos.onrender.com'

# ====================
# 📦 INSTALLED APPS
# ====================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'whitenoise.runserver_nostatic',
    'reservations',
]

# ====================
# ⚙️ MIDDLEWARE
# ====================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'conference_booking.urls'

# ====================
# 🧩 TEMPLATES
# ====================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'reservations.context_processors.site_settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'conference_booking.wsgi.application'

# ====================
# 🗄️ DATABASE (Supabase - Direct)
# ====================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres.goivdkqtcqajqxshldds',
        'PASSWORD': 'Kalumeemmanuel21@',
        'HOST': 'aws-1-ca-central-1.pooler.supabase.com',
        'PORT': '6543',
        'OPTIONS': {
            'sslmode': 'require',
        },
    }
}

# ====================
# 🔐 PASSWORD VALIDATION
# ====================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ====================
# 🌍 INTERNATIONALISATION
# ====================
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Africa/Kinshasa'
USE_I18N = True
USE_TZ = True

# ====================
# 📁 STATIC FILES
# ====================
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / "static"]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ====================
# 📂 MEDIA FILES
# ====================
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ====================
# 🔐 LOGIN
# ====================
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/login/'

# ====================
# 📧 EMAIL (Gmail direct)
# ====================
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'johnkalumeemmanuel9@gmail.com'
EMAIL_HOST_PASSWORD = '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' # Sans espaces
DEFAULT_FROM_EMAIL = 'johnkalumeemmanuel9@gmail.com'
CONTACT_EMAIL = 'johnkalumeemmanuel9@gmail.com'
# ====================
# 🔧 CUSTOM SETTINGS
# ====================
PRIX_PAR_PLACE = 7
MAX_PLACES_PAR_RESERVATION = 10
RESERVATION_EXPIRATION_HOURS = 24

# ====================
# 📱 TIMELINESAI WHATSAPP API
# ====================
TIMELINES_API_URL = 'https://waapi.app/api/v1/instances/ID/client/action/send-message'
TIMELINES_API_KEY = 'rFBXhMILLU4naah2bsCT5uAsjeGukQJWe2KzL0Brecb54d2c'
WHATSAPP_ACCOUNT_PHONE = '243859323184'
WHATSAPP_API_TYPE = 'timelines'

# ====================
# 🗑️ DEFAULT AUTO FIELD
# ====================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

print("✅ Configuration chargée avec succès !")
