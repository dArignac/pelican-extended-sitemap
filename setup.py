#!/usr/bin/env python
import codecs

from setuptools import setup


with codecs.open('README.rst', encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='pelican-extended-sitemap',
    description='sitemap generator plugin for pelican',
    # @see http://semver.org/
    version='1.2.2',
    author='Alexander Herrmann',
    author_email='darignac@gmail.com',
    license='MIT',
    url='https://github.com/dArignac/pelican-extended-sitemap',
    long_description=long_description,
    packages=[
        'extended_sitemap',
        'extended_sitemap.tests',
    ],
    package_data={
        'extended_sitemap': [
            'sitemap-stylesheet.xsl',
            'tests/content/articles/*.md',
            'tests/content/pages/*.md',
            'tests/expected/*.xml',
        ],
    },
    requires=[
        'pelican'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Text Processing :: Markup'
    ]
)
