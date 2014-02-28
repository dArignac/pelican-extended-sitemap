# -*- coding: utf-8 -*-
import datetime
import os

from codecs import open

from pelican import signals

from urlparse import urljoin


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
        self.url_site = settings.get('SITEURL')
        self.url_tags = urljoin(self.url_site, settings.get('TAGS_URL', 'tags.html'))
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

        def content_datetime_compare(x, y):
            """
            Compares two pelican.contents.Content classes with each other based on their date property.
            :param x: first content element
            :type x: pelican.contents.Content
            :param y: second content element
            :type x: pelican.contents.Content
            :returns: if x is before y
            :rtype: bool
            """
            return x.date > y.date

        # get all articles sorted by time
        articles_sorted = sorted(self.context['articles'], cmp=content_datetime_compare)

        # comprehend and sort tags
        tags_sorted = self.__comprehend_urlwrappers(self.context.get('tags'))

        # the landing page
        if 'index' in self.context.get('DIRECT_TEMPLATES'):
            # assume that the index page has changed with the most current article
            urls += self.__create_url_node_for_content(articles_sorted[0], 'index', overwrite_url=self.context.get('SITEURL'))

        # process articles
        for article in articles_sorted:
            urls += self.__create_url_node_for_content(article, 'articles')

        # process pages
        for page in sorted(self.context['pages'], cmp=content_datetime_compare):
            urls += self.__create_url_node_for_content(page, 'pages')

        # process configured index pages
        for element in self.context.get('DIRECT_TEMPLATES'):
            if element == 'tags':
                urls += self.__create_url_node_for_content(tags_sorted[0][0], 'others', overwrite_url=self.url_tags)
            elif element == 'categories':
                # TODO implement
                pass
            elif element == 'authors':
                # TODO implement
                pass
            elif element == 'archives':
                # TODO implement
                pass

        # write the final sitemap file
        with open(os.path.join(self.path_output, 'sitemap.xml'), 'w', encoding='utf-8') as fd:
            fd.write(self.xml_wrap % {
                'SITEURL': self.url_site,
                'urls': urls
            })

    @staticmethod
    def __comprehend_urlwrappers(urlwrappers):
        """
        Fetches all urlwrapper elements (tags, categories, archives) from the given wrapper based tupled list and creates a single list entry for each article
        the wrapper belongs to as (<article>, <wrapper>) tuple.
        :param urlwrappers: list of urlwrapper object as given by generator init method context
        :type urlwrappers: mixed
        :return: list of tuples
        :rtype: list
        """
        list_sorted = []
        for wrapper in urlwrappers:
            for article in wrapper[1]:
                list_sorted.append((article, wrapper[0]))

        list_sorted.sort(key=lambda x: x[0].date)
        list_sorted.reverse()
        return list_sorted

    def __create_url_node_for_content(self, content, content_type, overwrite_url=None):
        """
        Creates the required <url> node for the sitemap xml.
        :param content: the content class to handle
        :type content: pelican.contents.Content
        :param content_type: the type of the given content to match settings.EXTENDED_SITEMAP_PLUGIN
        :type content_type; str
        :param overwrite_url; if given, the URL to use instead of the url of the content instance
        :type overwrite_url: str
        :returns: the text node
        :rtype: str
        """
        return self.template_url % {
            'loc': overwrite_url if overwrite_url is not None else urljoin(self.url_site, self.context.get('ARTICLE_URL').format(**content.url_format)),
            # W3C YYYY-MM-DDThh:mm:ssTZD
            'lastmod': content.date.strftime('%Y-%m-%dT%H:%M:%S%z'),
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