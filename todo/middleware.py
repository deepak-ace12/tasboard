import os
import re
from datetime import datetime
from Dashboard import settings

from django.contrib.auth import logout
from django.urls import reverse
from django.shortcuts import redirect

import logging


log = logging.getLogger(__name__)
EXEMPT_URLS = [re.compile(settings.LOGIN_URL.lstrip('/'))]

if hasattr(settings, 'LOGIN_EXEMPT_URLS'):
    EXEMPT_URLS += [re.compile(url) for url in settings.LOGIN_EXEMPT_URLS]


class LoginRequiredMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        assert hasattr(request, 'user')
        path = request.path_info.lstrip('/')

        url_is_exempt = any(url.match(path) for url in EXEMPT_URLS)

        if path == reverse('todo:logout').lstrip('/'):
            logout(request)

        if not request.user.is_authenticated() and not url_is_exempt:
            return redirect(settings.LOGIN_URL)

        if request.user.is_authenticated() and url_is_exempt:
            return redirect(settings.LOGIN_REDIRECT_URL)

        elif request.user.is_authenticated() or url_is_exempt:
            return None

        else:
            return redirect(settings.LOGIN_URL)


class LoggingMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.process_response(request, self.get_response(request))
        return response

    def process_response(self, request, response):
        if request.user.is_authenticated:
            log.info("%s %s %s %s %s %s %s" % (
                datetime.now().time(), request.method,
                request.user.get_full_name(), request.user.email,
                response.status_code, request.get_full_path(), "\n")
            )
        return response
