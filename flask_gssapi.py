# -*- encoding: utf-8; -*-
# pylint: disable=R0201, W0212
"""GSSAPI authentication plugin for Flask"""

import base64
import socket
from functools import wraps

import gssapi
from flask import current_app, make_response, request, Response

__version__ = '1.5.0'


class GSSAPI(object):
    """
        Negotiate (GSSAPI) authentication extension for Flask applications for
        authenticating directory accounts under Microsoft Active Directory,
        Samba or FreeIPA.

    """
    def __init__(self, app=None, login_manager=None):
        self.app = app

        if app is not None:
            self.init_app(app, login_manager)

    def init_app(self, app, login_manager):
        """
        Initialises the Negotiate extension for the given application.
        """
        if not hasattr(app, 'extensions'):
            app.extensions = {}

        service_name = app.config.get('GSSAPI_SERVICE_NAME', 'HTTP')
        name = app.config.get('GSSAPI_HOSTNAME', socket.getfqdn())
        if name is not None:
            principal = '{}@{}'.format(service_name, name)
            name = gssapi.Name(principal, gssapi.NameType.hostbased_service)

        app.extensions['gssapi'] = {
            'creds': gssapi.Credentials(name=name, usage='accept'),
            'login_manager': login_manager,
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
                username = ctx.initiator_name
                return str(username), out_token

        return None, None

    def require_auth(self, *, username_arg='username'):
        """A decorator to protect views with Negotiate authentication."""
        return self.require_user(username_arg=username_arg)

    def require_user(self, *users, user=None, username_arg='username'):
        """A decorator to protect views with Negotiate authentication."""

        # accept old-style single user keyword-argument as well
        if user:
            users = (*users, user)

        def _require_auth(view_func):
            @wraps(view_func)
            def wrapper(*args, **kwargs):
                """ Effective wrapper """
                username, out_token = self.authenticate()
                if username:
                    if not users or username in users:
                        request.environ['REMOTE_USER'] = username
                        if username_arg:
                            kwargs[username_arg] = username
                        response = make_response(view_func(*args, **kwargs))
                    else:
                        response = Response(status=403)
                    if out_token:
                        b64_token = base64.b64encode(out_token).decode('utf-8')
                        auth_data = 'Negotiate {0}'.format(b64_token)
                        response.headers['WWW-Authenticate'] = auth_data
                    return response

                login_manager = current_app.extensions['gssapi']['login_manager']
                if login_manager:
                    resp = login_manager.unauthorized()
                    resp.headers['WWW-Authenticate'] = 'Negotiate'
                else:
                    return Response(
                        status=401,
                        headers={'WWW-Authenticate': 'Negotiate'},
                    )

            return wrapper
        return _require_auth
