pelican-extended-sitemap
========================

A sitemap plugin for `Pelican`_.

It generates a sitemap.xml according to the specification of `sitemaps.org`_ and considers the pelican index page, articles, pages and special pages (like tags, categories, authors).
Also comes with a XML stylesheet to be able to view the sitemap in browser without pain.

There is also a `sitemap plugin`_ within the official pelican plugin repo. The main differences in my package are:

* the overview pages for tags, pages aso are included
* there is a stylesheet
* used dates do not include time

**NOTICE: Backwards incompatible changes in 1.0.0:**

In version 1.0.0 the package naming has been fixed, it's now called "extended_sitemap" (instead "extended-sitemap") following PEP8.
Please adjust your usages in *PLUGINS* appropriately.

Sources and Status
------------------

.. image:: https://travis-ci.org/dArignac/pelican-extended-sitemap.svg?branch=master
    :target: https://travis-ci.org/dArignac/pelican-extended-sitemap
.. image:: https://coveralls.io/repos/dArignac/pelican-extended-sitemap/badge.png?branch=master
    :target: https://coveralls.io/r/dArignac/pelican-extended-sitemap?branch=master

* Github: `https://github.com/dArignac/pelican-extended-sitemap`_
* PyPI: `https://pypi.python.org/pypi/pelican-extended-sitemap`_

Pelican settings
----------------

Add to the plugins list:


.. code-block:: python

    PLUGINS = [
        'extended_sitemap'
    ]


Plugin settings
---------------

Add the `EXTENDED_SITEMAP_PLUGIN` dict to your settings.
The keys explained:

* priorities: priority for each page type, from 0.0 to 1.0
  
  * index: index page
  * articles: article pages
  * pages: pages
  * others: category, tags and authors pages
  
* changefrequencies: how often a page will likely change, possible values: always, hourly, daily, weekly, monthly, yearly, never

The settings below are the default values:

.. code-block:: python

    EXTENDED_SITEMAP_PLUGIN = {
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

Paths for DIRECT_TEMPLATES
~~~~~~~~~~~~~~~~~~~~~~~~~~
The value of the paths for `DIRECT_TEMPLATES`_ are defined by the following order:

(``{NAME}`` stands for the direct template name, e.g. ``ARCHIVES`` for archives.)

1. if the setting ``{NAME}_URL`` is defined, use ``{NAME}_URL``
2. if the setting ``{NAME}_URL`` is not defined but the setting ``{NAME}_SAVE_AS`` is, use ``{NAME}_SAVE_AS``
3. if none of the above applies, use the default filename ``{NAME}.html``

Note that ``{NAME}_URL`` is not a default Pelican setting.


Tests
-----

`nose`_ is required to run the tests. Install the package and run with the *nosetest* command.

The tests fixture files were created with generated content by http://jaspervdj.be/lorem-markdownum/.

Changelog
---------
see `Github release page`_.


ToDos
-----

What still has to be implemented:

* support for multilingual content, see `pelican translations`_ (it in fact may work, but I have not tested it)

Contributors
------------
**Thanks to all contributers!**

* `dArignac <https://github.com/dArignac>`__  (Owner)
* `wamomite <https://github.com/wamonite>`__ (`Pull Request #8 <https://github.com/dArignac/pelican-extended-sitemap/pull/8>`__)
* `wAmpIre <https://github.com/wAmpIre>`__ (`Pull Request #9 <https://github.com/dArignac/pelican-extended-sitemap/pull/9>`__)

Bug Reporters:

* `jakub-olczyk <https://github.com/jakub-olczyk>`__
* `VorpalBlade <https://github.com/VorpalBlade>`__


.. _Pelican: https://github.com/getpelican/pelican
.. _sitemaps.org: http://sitemaps.org
.. _sitemap plugin: https://github.com/getpelican/pelican-plugins/tree/master/sitemap
.. _pelican translations: http://docs.getpelican.com/en/3.3.0/getting_started.html#translations
.. _https://github.com/dArignac/pelican-extended-sitemap: https://github.com/dArignac/pelican-extended-sitemap
.. _https://pypi.python.org/pypi/pelican-extended-sitemap: https://pypi.python.org/pypi/pelican-extended-sitemap
.. _nose: https://nose.readthedocs.org/en/latest/
.. _Github release page: https://github.com/dArignac/pelican-extended-sitemap/releases
.. _DIRECT_TEMPLATES: https://docs.getpelican.com/en/stable/settings.html?highlight=DIRECT_TEMPLATES#template-pages