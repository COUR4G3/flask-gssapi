from setuptools import setup

from flask_gssapi import __version__ as version

setup(
    name='Flask-GSSAPI',
    version=version,
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
