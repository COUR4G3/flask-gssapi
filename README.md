# Flask-SPNEGO

__This extension has not been extensively tested and a good understanding of
Python, GSSAPI and Negotiate authentication is recommended.__

HTTP Negotiate (SPNEGO) authentication support for Flask applications. Secure
sensitive views or your entire application to with transparent and secure
Single-Sign-On to authorize and identify users.

The authentication scheme is widely supported across operating systems, browsers
and directory services and supports both Windows Integrated Auth and MIT/Heimdal
Kerberos clients (Windows, Linux, Mac OSX) and every mainstream browser so is a
perfect fit for an organization that has implemented a Microsoft or Samba Active
Directory server to manage users.

This extension only implements authentication, it does not handle authorization,
permissions or user identity besides providing the peer name to be processed by
your application and whatever code or extension you use to handle permissions
and user identity.

## Installation

Install the easy way through PyPi:

    pip install flask-spnego

Or alternatively download and build yourself:

```
   git clone https://github.com/cour4g3/flask-spnego
   cd flask-spnego
   python setup.py install
```

## Usage

Usage is fairly simple:

```python
from flask import Flask, render_template
from flask.ext.negotiate import Negotiate

app = Flask(__name__)

negotiate = Negotiate(app)

@app.route('/secret')
@negotiate.require_auth
def secret_view():
    return render_template('secret.html')
```

## Configuration

By default the module will point to the default keytab which your application
__should not__ have any access to. You should create a new keytab for your
application that only the running user has access to:

    KRB5_KTNAME=FILE:/path/to/HTTP.keytab
    net ads keytab create
    net ads keytab add HTTP
    chown httpd:httpd /path/to/HTTP.keytab

The `KRB5_KTNAME` will point to the correct keytab to use and can be included
in your startup script or service file.

The defaults should be sufficient for most purposes, but you may need to be
changed under certain circumstances:

|`NEGOTIATE_AUTH_PRINCIPAL`|The service principal you want to authenticate against. Defaults to `HTTP@$FQDN` where $FQDN is the value provided by `socket.getfqdn`.|

## Todo

- Testing with Windows and Linux clients and browsers has been done, but testing
  is required with Mac OS X as well as with a Windows-based server
  implementation.
- Expose the peer name to the Flask application via one or more mechanisms.
- Consider allowing short-lived sessions instead of authenticating on every
  single request; though with Keep-Alive and intranet connections this
  shouldn't be an issue.
- Offer a fallback authentication option for clients that do not support
  Negotiate authentication. Or make it play nice with another Flask
  authentication extension that can be used as fallback?

## License

Licensed under the MIT License.
