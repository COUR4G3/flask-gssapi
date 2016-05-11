import base64
from flask import abort, current_app, make_response, request, Response
from functools import wraps
import gssapi
import os
from socket import getfqdn

__version__ = '0.1'

class Negotiate(object):
    """
    Negotiate authentication extension for Flask applications. Provides support
    for SSO enterprise authentication via an SPNEGO/GSSAPI through Microsoft
    Active Directory or Samba.
    """
    def __init__(self, app=None):
        self.app = app

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """
        Initialises the Negotiate extension for the given application.
        """
        self.app = app

        principal = app.config.get('NEOGOTIATE_AUTH_PRINCIPAL', '%s@%s' % (
            'HTTP', getfqdn()))

        name = gssapi.Name(principal, gssapi.NameType.hostbased_service)
        self.credentials = gssapi.Credentials(name=name, usage='accept')

    def authenticate(self):
        """
        Attempts to authenticate the user if a token was provided.
        """
        if request.headers.get('Authorization', '').startswith('Negotiate '):
            in_token = base64.b64decode(request.headers['Authorization'][10:])

            ctx = gssapi.SecurityContext(creds=self.credentials, usage='accept')

            out_token = ctx.step(in_token)
            if ctx.complete and out_token:
                return True, out_token
            elif out_token:
                return False, out_token
        return False, ''

    def require_auth(self, view_func):
        """
        A decorator to protect views with Negotiate authentication.
        """
        @wraps(view_func)
        def wrapper(*args, **kwargs):
            success, out_token = self.authenticate()
            if success:
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
