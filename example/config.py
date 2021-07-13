import os
import base64
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.flaskenv'))

class Config(object):

    # Setup Secret Key for Application
    SECRET_KEY = os.environ.get('SECRET_KEY') or str(base64.b64encode('you-will-never-guess'.encode("utf-8")))

    # The service name you want to authenticate against
    # GSSAPI_SERVICE_NAME = 'HTTP'

    # The hostname you want authenticate against
    # GSSAPI_HOSTNAME = '...'