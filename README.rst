Flask-GSSAPI
############
HTTP Negotiate (GSSAPI) authentication support for Flask applications. Secure
sensitive views with transparent and secure single sign-on to authorize user
access using existing access controls within your Microsoft, Samba Active
Directory or FreeIPA servers.

Currently the username and ticket are not exposed to your application, however
this should be possible. It also does not offer more fine-grained permission
systems to user groups, only the host-based and service-based access controls
implemented by your authentication server.

Installation
============
Install the easy way through PyPi:

.. code-block:: console

  $ pip install flask-gssapi

Or alternatively download and build yourself:

.. code-block:: console

  $ git clone https://github.com/cour4g3/flask-gssapi
  $ cd flask-gssapi
  $ python setup.py install

Usage
=====
Usage is fairly simple:

.. code-block:: python

  from flask import Flask, render_template
  from flask_gssapi import GSSAPI

  app = Flask(__name__)

  gssapi = GSSAPI(app)

  # Here, you'll need to be authenticated
  @app.route('/secret')
  @gssapi.require_auth
  def secret_view():
      return render_template('secret.html')

  # Here, you'll need to be a specific user
  @app.route('/admin')
  @gssapi.require_user(user=admin)
  def admin_view():
      return render_template('admin.html')

Configuration
=============
For security purposes your application should probably not have read access to
the system's keytab, you should create a new keytab for the application:

.. code-block:: console

  $ export KRB5_KTNAME=FILE:/path/to/HTTP.keytab
  $ net ads keytab create
  $ net ads keytab add HTTP
  $ chown httpd:httpd /path/to/HTTP.keytab

The `KRB5_KTNAME` will point to the correct keytab to use and can be included
in your startup script or service file.

The defaults should be sufficient for most purposes, but you may need to be
changed under certain circumstances:

+-----------------------+------------------------------------------------------+
| Key                   | Description                                          |
+=======================+======================================================+
| `GSSAPI_SERVICE_NAME` | The service name you want to authenticate against,   |
|                       | by default this is `HTTP` which most browsers use.   |
+-----------------------+------------------------------------------------------+
| `GSSAPI_HOSTNAME`     | The hostname you want authenticate against, by       |
|                       | default this is acquired from `socket.fqdn()`.       |
+-----------------------+------------------------------------------------------+

Todo
====
* Offer fallback to a login page or Basic authentication if no credentials are
  provided i.e. non-domain connected device.
* Configuration key to protect all views by default with an equivalent `no_auth`
  decorator.

License
=======
Licensed under the MIT License.
