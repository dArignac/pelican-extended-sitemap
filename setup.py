#!/usr/bin/env python
import codecs
import os
import re

from setuptools import setup


with codecs.open('README.rst', encoding='utf-8') as f:
    long_description = f.read()


def get_version():
    """
    Returns the version of the package from the __init__ file.
    :return: version number
    :rtype: str
    """
    with codecs.open(os.path.join(os.path.dirname(__file__), 'extended-sitemap', '__init__.py'), encoding='utf-8') as f:
        version_file = f.read()
        version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
        if version_match:
            return version_match.group(1)
        raise RuntimeError('Unable to fetch version')


setup(
    name='pelican-extended-sitemap',
    description='sitemap generator plugin for pelican',
    version=get_version(),
    author='Alexander Herrmann',
    author_email='darignac@gmail.com',
    license='MIT',
    url='https://github.com/dArignac/pelican-extended-sitemap',
    long_description=long_description,
    packages=[
        'extended-sitemap',
    ],
    package_data={
        'extended-sitemap': [
            'sitemap-stylesheet.xsl'
        ],
    },
    requires=[
        'Pelican'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Text Processing :: Markup'
    ]
)
