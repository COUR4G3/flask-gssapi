import base64
import gssapi
import os
import socket

from flask import abort, current_app, make_response, request, Response
from functools import wraps

__version__ = '1.0'

class GSSAPI(object):
    """
        Negotiate (GSSAPI) authentication extension for Flask applications for
        authenticating directory accounts under Microsoft Active Directory,
        Samba or FreeIPA.

    """
    def __init__(self, app=None):
        self.app = app

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """
        Initialises the Negotiate extension for the given application.
        """
        if not hasattr(app, 'extensions'):
            app.extensions = {}

        service_name = app.config.get('GSSAPI_SERVICE_NAME', 'HTTP')
        hostname = app.config.get('GSSAPI_HOSTNAME', socket.getfqdn())
        principal = '{}@{}'.format(service_name, hostname)
        name = gssapi.Name(principal, gssapi.NameType.hostbased_service)

        app.extensions['gssapi'] = {
            'creds': gssapi.Credentials(name=name, usage='accept'),
        }

    def authenticate(self):
        """Attempts to authenticate the user if a token was provided."""
        if request.headers.get('Authorization', '').startswith('Negotiate '):
            in_token = base64.b64decode(request.headers['Authorization'][10:])

            try:
                creds = current_app.extensions['gssapi']['creds']
            except KeyError:
                raise RuntimeError('flask-gssapi not configured for this app')

            ctx = gssapi.SecurityContext(creds=creds, usage='accept')

            out_token = ctx.step(in_token)

            if ctx.complete:
                return out_token

        return False

    def require_auth(self, view_func):
        """A decorator to protect views with Negotiate authentication."""
        @wraps(view_func)
        def wrapper(*args, **kwargs):
            out_token = self.authenticate()
            if out_token:
                response = make_response(view_func(*args, **kwargs))
                response.headers['WWW-Authenticate'] = 'Negotiate ' + \
                    base64.b64encode(out_token).decode('utf-8')
                return response
            else:
                return Response(
                    status=401,
                    headers={'WWW-Authenticate': 'Negotiate' if not out_token \
                        else 'Negotiate ' + base64.b64encode(out_token).decode('utf-8')},
                )

        return wrapper
