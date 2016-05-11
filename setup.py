import os
import re

from setuptools import setup

def get_version():
    pattern = re.compile(r'__version__\s+=\s+[\'\"](.*)[\'\"]')
    with open('flask_spnego.py', 'r') as lines:
        for line in lines:
            match = re.search(pattern, line)
            if match:
                return match.groups()[0].strip()
    raise Exception('Cannot find version')

setup(
    name='Flask-SPNEGO',
    version=get_version(),
    url='https://github.com/cour4g3/flask-spnego',
    license='MIT',
    author='Michael de Villiers',
    author_email='twistedcomplexity@gmail.com',
    description='HTTP Negotiate (SPNEGO) authentication support for Flask applications.',
    long_description=open('README.md', 'r').read(),
    py_modules=['flask_spnego'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask',
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
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
