# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

import locale
import os
import unittest

from extended_sitemap import ConfigurationError

from tempfile import mkdtemp

from pelican import Pelican
from pelican.settings import read_settings
from pelican.tests.support import mute


# used paths
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
CONTENT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, 'content'))
OUTPUT_PATH = os.path.abspath(os.path.join(CURRENT_DIR, 'output'))

# TODO ensure Python 3 works, too


class ExtendedSitemapTest(unittest.TestCase):

    def setUp(self):
        self.path_temp = mkdtemp(prefix='extended_sitemap_tests.')
        self.path_cache = mkdtemp(prefix='extended_sitemap_cache.')

        # default minimal configuration for pelican in test context
        self.settings_default = {
            'PAGE_DIR': os.path.join(CONTENT_DIR, 'pages'),
            'ARTICLE_DIR': os.path.join(CONTENT_DIR, 'articles'),
            'PATH': CONTENT_DIR,
            'OUTPUT_PATH': self.path_temp,
            'CACHE_PATH': self.path_cache,
            'LOCALE': locale.normalize('en_US'),
            'PLUGIN_PATH': os.path.join(CURRENT_DIR, '..'),
            'PLUGINS': ['extended_sitemap'],
        }

    def __execute_pelican(self, settings_override=None):
        """
        Executes pelican. Uses the minimal config of self.settings_default (that will fail!) merged with the given additional settings.
        :param settings_override: dictionary with pelican setting values to set
        :type settings_override: dict
        """
        if not settings_override:
            settings_override = {}
        settings = read_settings(
            path=None,
            override=dict(self.settings_default.items() + settings_override.items())
        )
        pelican = Pelican(settings=settings)
        mute(True)(pelican.run)()

    def test_timezone_missing(self):
        """
        As the TIMEZONE settings is necessary to create timezone based date value, ensure the configuration exception is raised if it is not configured.
        """
        self.assertRaises(ConfigurationError, self.__execute_pelican)

    # TODO remove
    def test_something(self):
        self.__execute_pelican(settings_override={'TIMEZONE': 'Europe/Berlin'})
        self.assertTrue(True)
