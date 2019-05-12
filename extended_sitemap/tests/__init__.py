# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

import filecmp
import locale
import os
import re
import subprocess
import sys
import unittest

from extended_sitemap import ConfigurationError

from functools import wraps

from tempfile import mkdtemp

from pelican import Pelican
from pelican.settings import read_settings

from six import StringIO

# used paths
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
CONTENT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, 'content'))
EXPECTED_DIR = os.path.abspath(os.path.join(CURRENT_DIR, 'expected'))
OUTPUT_PATH = os.path.abspath(os.path.join(CURRENT_DIR, 'output'))


def isplit(s, sep=None):
    """Behaves like str.split but returns a generator instead of a list.
    >>> list(isplit('\tUse the force\n')) == '\tUse the force\n'.split()
    True
    >>> list(isplit('\tUse the force\n')) == ['Use', 'the', 'force']
    True
    >>> (list(isplit('\tUse the force\n', "e"))
         == '\tUse the force\n'.split("e"))
    True
    >>> list(isplit('Use the force', "e")) == 'Use the force'.split("e")
    True
    >>> list(isplit('Use the force', "e")) == ['Us', ' th', ' forc', '']
    True
    """
    sep, hardsep = r'\s+' if sep is None else re.escape(sep), sep is not None
    exp, pos, l = re.compile(sep), 0, len(s)
    while True:
        m = exp.search(s, pos)
        if not m:
            if pos < l or hardsep:
                #      ^ mimic "split()": ''.split() returns []
                yield s[pos:]
            break
        start = m.start()
        if pos < start or hardsep:
            #           ^ mimic "split()": includes trailing empty string
            yield s[pos:start]
        pos = m.end()


def mute(returns_output=False):
    """Decorate a function that prints to stdout, intercepting the output.
    If "returns_output" is True, the function will return a generator
    yielding the printed lines instead of the return values.
    The decorator literally hijack sys.stdout during each function
    execution, so be careful with what you apply it to.
    >>> def numbers():
        print "42"
        print "1984"
    ...
    >>> numbers()
    42
    1984
    >>> mute()(numbers)()
    >>> list(mute(True)(numbers)())
    ['42', '1984']
    """

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            saved_stdout = sys.stdout
            sys.stdout = StringIO()

            try:
                out = func(*args, **kwargs)
                if returns_output:
                    out = isplit(sys.stdout.getvalue().strip())
            finally:
                sys.stdout = saved_stdout

            return out

        return wrapper

    return decorator


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
        pelican.run()

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

    def test_sitemap_structure_custom_article_url(self):
        """
        Tests basic structure of generated sitemap with customized ARTICLE_URL and ARTICLE_SAVE_AS settings.
        """
        # issue #2
        self.__execute_pelican(
            settings_override={
                'TIMEZONE': 'Europe/Berlin',
                'ARTICLE_URL': 'customarticles/{date:%Y}/{date:%b}/{date:%d}/{slug}/',
                'ARTICLE_SAVE_AS': '{slug}.custom.html',
            }
        )
        self.assertFileContentEquals(
            os.path.join(EXPECTED_DIR, 'test_sitemap_structure_custom_article_url.xml'),
            os.path.join(self.path_temp, 'sitemap.xml')
        )

    def test_sitemap_structure_with_custom_direct_templates_filenames(self):
        """
        Tests sitemap structure with custom %s_SAVE_AS values for DIRECT_TEMPLATES.
        Source: https://github.com/dArignac/pelican-extended-sitemap/issues/14
        """
        self.__execute_pelican(
            settings_override={
                'TIMEZONE': 'Europe/Berlin',
                'TAGS_SAVE_AS': 'abc/tags.html',
                'CATEGORIES_SAVE_AS': 'cats/meow/something.txt',
                'AUTHORS_SAVE_AS': 'those-writers.html',
                'ARCHIVES_SAVE_AS': 'our-curated-library.html',
            }
        )
        self.assertFileContentEquals(
            os.path.join(EXPECTED_DIR, 'test_sitemap_structure_direct_templates_1.xml'),
            os.path.join(self.path_temp, 'sitemap.xml')
        )

    def test_sitemap_structure_with_custom_direct_templates_urls(self):
        """
        Tests sitemap structure with custom %s_URL values for DIRECT_TEMPLATES.
        Source: https://github.com/dArignac/pelican-extended-sitemap/issues/15
        """
        self.__execute_pelican(
            settings_override={
                'TIMEZONE': 'Europe/Berlin',
                'TAGS_URL': 'abc/tags',
                'CATEGORIES_URL': 'cats/meow',
                'AUTHORS_URL': 'authors/all',
                'ARCHIVES_URL': 'lib/the-archive/list/',
                # also define the SAVE_AS to test correct resolution sorting
                'TAGS_SAVE_AS': 'abc/tags.html',
                'CATEGORIES_SAVE_AS': 'cats/meow/something.txt',
                'AUTHORS_SAVE_AS': 'those-writers.html',
                'ARCHIVES_SAVE_AS': 'our-curated-library.html',
            }
        )
        self.assertFileContentEquals(
            os.path.join(EXPECTED_DIR, 'test_sitemap_structure_direct_templates_2.xml'),
            os.path.join(self.path_temp, 'sitemap.xml')
        )
