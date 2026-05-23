from django.conf import settings

def site_settings(request):
    return {
        'SITE_URL': settings.SITE_URL,
        'SITE_NAME': 'Conference Booking',
        'MEDIA_URL': settings.MEDIA_URL,
        'STATIC_URL': settings.STATIC_URL,
    }