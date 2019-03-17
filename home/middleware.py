from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
import requests

class MultipleProxyMiddleware(MiddlewareMixin):
    FORWARDED_FOR_FIELDS = [
        'HTTP_X_FORWARDED_FOR',
        'HTTP_X_FORWARDED_HOST',
        'HTTP_X_FORWARDED_SERVER',
    ]

    def process_request(self, request):
        """
        Rewrites the proxy headers so that only the most
        recent proxy is used.
        """
        for field in self.FORWARDED_FOR_FIELDS:
            if field in request.META:
                if ',' in request.META[field]:
                    parts = request.META[field].split(',')
                    request.META[field] = parts[-1].strip()

class DefaultLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        # Set default language to Indonesian
        if request.session.get('language') is None:
            # Get location based on IP address
            ip = request.META.get('HTTP_X_FORWARDED_FOR', '') or request.META.get('REMOTE_ADDR')
            print(f'Detected ip is {ip}')
            ipstack_apikey = settings.IPSTACK_APIKEY
            ipstack = f'http://api.ipstack.com/{ip}?access_key={ipstack_apikey}'

            country_code = None
            try:
                r = requests.get(ipstack)
                country_code = r.json().get('country_code', None)
                print(f'Detected country code is {country_code}')
            except:
                print('ERROR: cannot use requests lib')
            
            if country_code is None or country_code == 'ID':
                request.session['language'] = 'id'
            else:
                request.session['language'] = 'en'

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
