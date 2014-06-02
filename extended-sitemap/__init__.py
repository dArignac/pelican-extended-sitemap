# -*- coding: utf-8 -*-

import datetime
import os
import sys

from codecs import open

from pelican import signals

from pytz import timezone

if sys.version_info >= (3, 0):
    from urllib.parse import urljoin
else:
    from urlparse import urljoin


__version__ = '0.2.0'


class SitemapGenerator(object):
    """
    Class for generating a sitemap.xml.
    """

    xml_wrap = """<?xml version="1.0" encoding="UTF-8"?><?xml-stylesheet type="text/xsl" href="%(SITEURL)s/sitemap-stylesheet.xsl"?>
<urlset xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd" xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
%(urls)s
</urlset>"""

    template_url = """<url>
<loc>%(loc)s</loc>
<lastmod>%(lastmod)s</lastmod>
<changefreq>%(changefreq)s</changefreq>
<priority>%(priority).2f</priority>
</url>"""

    settings_default = {
        'priorities': {
            'index': 1.0,
            'articles': 0.8,
            'pages': 0.5,
            'others': 0.4
        },
        'changefrequencies': {
            'index': 'daily',
            'articles': 'weekly',
            'pages': 'monthly',
            'others': 'monthly',
        }
    }

    def __init__(self, context, settings, path, theme, output_path, **kwargs):
        """
        Initializes the generator class.
        :param context: the generated context, mix of settings and transformed content
        :type context: dict
        :param settings: the pelican project settings
        :type settings: dict
        :param path: the path to the content files
        :type path: str
        :param theme: the path to the theme
        :type theme: str
        :param output_path: the path where the generated output is put
        :type output_path: str
        :param kwargs: additional keyword arguments
        :type kwargs: dict
        """
        self.path_content = path
        self.path_output = output_path
        self.context = context
        self.timezone = timezone(settings.get('TIMEZONE'))
        self.url_site = settings.get('SITEURL')
        self.settings = settings.get('EXTENDED_SITEMAP_PLUGIN', self.settings_default)

    def generate_output(self, writer):
        """
        Generates the sitemap file and the stylesheet file and puts them into the content dir.
        :param writer: the writer instance
        :type writer: pelican.writers.Writer
        """
        # write xml stylesheet
        with open(os.path.join(os.path.dirname(__file__), 'sitemap-stylesheet.xsl'), 'r', encoding='utf-8') as fd_origin:
            with open(os.path.join(self.path_output, 'sitemap-stylesheet.xsl'), 'w', encoding='utf-8') as fd_destination:
                xsl = fd_origin.read()
                # replace some template markers
                # TODO use pelican template magic
                xsl = xsl.replace('{{ SITENAME }}', self.context.get('SITENAME'))
                fd_destination.write(xsl)

        # will contain the url nodes as text
        urls = ''

        # get all articles sorted by time
        articles_sorted = sorted(self.context['articles'], key=lambda x: x.date, reverse=True)

        # the landing page
        if 'index' in self.context.get('DIRECT_TEMPLATES'):
            # assume that the index page has changed with the most current article
            urls += self.__create_url_node_for_content(
                articles_sorted[0],
                'index',
                url=self.url_site,
            )

        # process articles
        for article in articles_sorted:
            urls += self.__create_url_node_for_content(article, 'articles')

        # process pages
        for page in sorted(self.context.get('pages'), key=lambda x: x.date, reverse=True):
            urls += self.__create_url_node_for_content(
                page,
                'pages',
                url=urljoin(self.url_site, page.url)
            )

        # process category pages
        urls += self.__process_url_wrapper_elements(self.context.get('categories'))

        # process tag pages
        urls += self.__process_url_wrapper_elements(self.context.get('tags'))

        # process author pages
        urls += self.__process_url_wrapper_elements(self.context.get('authors'))

        # write the final sitemap file
        with open(os.path.join(self.path_output, 'sitemap.xml'), 'w', encoding='utf-8') as fd:
            fd.write(self.xml_wrap % {
                'SITEURL': self.url_site,
                'urls': urls
            })

    def __process_url_wrapper_elements(self, elements):
        """
        Creates the url nodes for pelican.urlwrappers.Category and pelican.urlwrappers.Tag.
        :param elements: list of wrapper elements
        :type elements: list
        :return: the processes urls as HTML
        :rtype: str
        """
        urls = ''
        for url_wrapper, articles in elements:
            urls += self.__create_url_node_for_content(
                url_wrapper,
                'others',
                url=urljoin(self.url_site, url_wrapper.url),
                modification_time=sorted(articles, key=lambda x: x.date, reverse=True)[0].date
            )
        return urls

    def __create_url_node_for_content(self, content, content_type, url=None, modification_time=None):
        """
        Creates the required <url> node for the sitemap xml.
        :param content: the content class to handle
        :type content: pelican.contents.Content
        :param content_type: the type of the given content to match settings.EXTENDED_SITEMAP_PLUGIN
        :type content_type; str
        :param url; if given, the URL to use instead of the url of the content instance
        :type url: str
        :param modification_time: the modification time of the url, will be used instead of content date if given
        :type modification_time: datetime.datetime
        :returns: the text node
        :rtype: str
        """
        return self.template_url % {
            'loc': url if url is not None else urljoin(self.url_site, self.context.get('ARTICLE_URL').format(**content.url_format)),
            'lastmod': self.timezone.localize(modification_time).isoformat() if modification_time is not None else self.timezone.localize(content.date).isoformat(),
            'changefreq': self.settings.get('changefrequencies').get(content_type),
            'priority': self.settings.get('priorities').get(content_type),
        }


def get_generators(generators):
    """
    Returns the generators of this plugin,
    :param generators: current generators
    :type generators: pelican.Pelican
    :returns: the sitemap generator type
    :rtype: type
    """
    return SitemapGenerator


def register():
    """
    Registers the sitemap generator.
    """
    signals.get_generators.connect(get_generators)