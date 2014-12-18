# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

import filecmp
import locale
import os
import subprocess
import unittest

from extended_sitemap import ConfigurationError

from tempfile import mkdtemp

from pelican import Pelican
from pelican.settings import read_settings
from pelican.tests.support import mute


# used paths
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
CONTENT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, 'content'))
EXPECTED_DIR = os.path.abspath(os.path.join(CURRENT_DIR, 'expected'))
OUTPUT_PATH = os.path.abspath(os.path.join(CURRENT_DIR, 'output'))


class FileComparisonTest(unittest.TestCase):
    """
    Unittest class with possibility to assert equal file contents.
    """
    def assertFileContentEquals(self, path_file_expected, path_file_test):
        """
        Asserts the file contents to be equal.
        :param path_file_expected: path to the file with the expected content
        :type path_file_expected: str
        :param path_file_test: path to the file to test
        :type path_file_test: str
        """
        if not filecmp.cmp(path_file_expected, path_file_test):
            msg_fail = 'File content of %(filename)s does not match expected content!' % {'filename': path_file_test}

            # if there is git and git diff works for both files, append the file diff to the fail message
            try:
                out, err = subprocess.Popen(
                    ['git', 'diff', '--minimal', '--no-color', '--no-ext-diff', '--exit-code', '-w', path_file_expected, path_file_test],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                ).communicate()
                if len(err) == 0:
                    msg_fail += '\n\n' + out.decode('utf-8')
            except OSError:
                # if there is no git, just don't output the diff
                pass

            self.fail(msg_fail)


class ExtendedSitemapTest(FileComparisonTest):

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
            'SITEURL': 'http://example.com',
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

        settings = self.settings_default.copy()
        settings.update(settings_override)

        pelican_settings = read_settings(
            path=None,
            override=settings
        )
        pelican = Pelican(settings=pelican_settings)
        mute(True)(pelican.run)()

    def test_timezone_missing(self):
        """
        As the TIMEZONE settings is necessary to create timezone based date value, ensure the configuration exception is raised if it is not configured.
        """
        self.assertRaises(ConfigurationError, self.__execute_pelican)

    def test_sitemap_structure(self):
        """
        Tests basic structure of generated sitemap.
        """
        self.__execute_pelican(
            settings_override={
                'TIMEZONE': 'Europe/Berlin',
            }
        )
        self.assertFileContentEquals(
            os.path.join(EXPECTED_DIR, 'test_sitemap_structure.xml'),
            os.path.join(self.path_temp, 'sitemap.xml')
        )

    def test_sitemap_structure_subpaths(self):
        """
        Tests basic structure of generated sitemap with subpath in domain.
        """
        # issue #2
        self.__execute_pelican(
            settings_override={
                'TIMEZONE': 'Europe/Berlin',
                'SITEURL': 'http://example.com/subpath',
            }
        )
        self.assertFileContentEquals(
            os.path.join(EXPECTED_DIR, 'test_sitemap_structure_subpath.xml'),
            os.path.join(self.path_temp, 'sitemap.xml')
        )
