1.0.2
-----
* fixed that if the following settings are not set, no sitemap entry is generated for the appropriate pages
    * CATEGORY_URL
    * TAG_URL
    * AUTHOR_URL

1.0.1
-----
* fixed compatibility with Pelican 3.5
* dates are now W3C compliant and do not include time
* adjusted setup.py

1.0.0
-----
* fixed wrong package naming, now "extended_sitemap" instead "extended-sitemap"
* added unit tests
* raise ConfigurationError if TIMEZONE setting is not set
* tags are now sorted by name

0.2.0
-----
* Python 3 support

0.1.4
-----
* fixed date format in sitemap
* changed xml stylesheet link for this package to PyPI

0.1.3
-----
* adjusted documentation

0.1.2
-----
* adjusted documentation

0.1.1
-----
* adjusted documentation

0.1.0
-----
* initial release covering index, articles, pages, categories, tags and author pages
