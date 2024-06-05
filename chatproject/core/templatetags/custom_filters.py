from django import template
import requests
from django.conf import settings
from urllib.parse import urljoin

register = template.Library()

@register.filter
def file_exists(image):
    base_url = getattr(settings, 'BASE_URL', '')
    full_url = urljoin(base_url,image)
    try:

        response = requests.head(full_url)
        return response.status_code == 200
    except requests.RequestException as exp:
        return False
