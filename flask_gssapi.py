# -*- encoding: utf-8; -*-
# pylint: disable=R0201, W0212
"""GSSAPI authentication plugin for Flask"""

import base64
import socket
from functools import wraps

import gssapi
from flask import current_app, make_response, request, Response

__version__ = '1.1'


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
                username = ctx._inquire(initiator_name=True).initiator_name
                return username, out_token

        return None, None

    def require_auth(self):
        """A decorator to protect views with Negotiate authentication."""
        return self.require_user()

    def require_user(self, user=None):
        """A decorator to protect views with Negotiate authentication.
           Enhanced version wich accept a user parameter to require a
           specific user.
        """
        def _require_auth(self, view_func):
            @wraps(view_func)
            def wrapper(*args, **kwargs):
                """ Effective wrapper """
                username, out_token = self.authenticate()
                if username and out_token:
                    b64_token = base64.b64encode(out_token).decode('utf-8')
                    auth_data = 'Negotiate {0}'.format(b64_token)
                    if not user or user == username:
                        response = make_response(view_func(*args, **kwargs))
                    else:
                        response = Response(status=403)
                    response.headers['WWW-Authenticate'] = auth_data
                    return response
                return Response(
                    status=401,
                    headers={'WWW-Authenticate': 'Negotiate'},
                )

            return wrapper
        return _require_auth
