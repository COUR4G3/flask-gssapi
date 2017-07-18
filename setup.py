from setuptools import setup

import io
import os
import os.path
import re

def long_description():
    descr = open('README.rst', 'r').read()

    try:
        descr += '\n\n' + open('docs/changelog.rst', 'r').read()
    except:
        pass

    return descr


def read(*names, **kwargs):
    with io.open(
        os.path.join(os.path.dirname(__file__), *names),
        encoding=kwargs.get("encoding", "utf8") 
    ) as fp:
        return fp.read()

def find_version(file_path):
    version_file = read(file_path)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

setup(
    name='Flask-GSSAPI',
    version=find_version('flask_gssapi.py'),
    url='https://github.com/cour4g3/flask-gssapi',
    license='MIT',
    author='Michael de Villiers',
    author_email='michael@cour4g3.me',
    description='HTTP Negotiate (GSSAPI) authentication support for Flask applications.',
    long_description=open('README.rst', 'r').read(),
    py_modules=['flask_gssapi'],
    platforms='any',
    install_requires=[
        'flask',
        'gssapi',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
