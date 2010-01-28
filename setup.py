#!/usr/bin/env python
# -*- coding: utf-8 -*-
from distutils.core import setup

setup(
    name='saved_searches',
    version='1.0.0',
    description='Saves user searches for integration with Haystack.',
    author='Daniel Lindsley',
    author_email='daniel@toastdriven.com',
    url='http://github.com/toastdriven/saved_searches',
    packages=[
        'saved_searches',
        'queued_search.templatetags',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities'
    ],
)
