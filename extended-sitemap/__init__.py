# -*- coding: utf-8 -*-
import os

from codecs import open

from pelican import signals, contents
from pelican.utils import get_date


class SitemapGenerator(object):

    xml_wrap = """<?xml version="1.0" encoding="UTF-8"?><?xml-stylesheet type="text/xsl" href="%(SITEURL)s/sitemap-stylesheet.xsl"?>
<urlset xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd" xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
%(urls)s
</urlset>"""

    def __init__(self, context, settings, path, theme, output_path, **kwargs):
        self.path_content = path
        self.path_output = output_path
        self.context = context

    def generate_output(self, writer):
        # from pprint import pprint
        # pprint(self.context, indent=4)

        # write xml stylesheet
        with open(os.path.join(os.path.dirname(__file__), 'sitemap-stylesheet.xsl'), 'r', encoding='utf-8') as fd_org:
            with open(os.path.join(self.path_output, 'sitemap-stylesheet.xsl'), 'w', encoding='utf-8') as fd_dest:
                xsl = fd_org.read()
                # replace some template markers
                # TODO use pelican template magic
                xsl = xsl.replace('{{ SITENAME }}', self.context['SITENAME'])
                fd_dest.write(xsl)

        # for article in self.context['articles']:
        #     print type(article)
        with open(os.path.join(self.path_output, 'sitemap.xml'), 'w', encoding='utf-8') as fd:
            fd.write(self.xml_wrap % {
                'SITEURL': self.context['SITEURL'],
                # TODO read something real ;-)
                'urls': '<url><loc>http://www.example.com/</loc><lastmod>2005-01-01</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url><url><loc>http://www.example.com/</loc><lastmod>2006-01-01</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>'
            })


def get_generators(generators):
    return SitemapGenerator


def register():
    signals.get_generators.connect(get_generators)