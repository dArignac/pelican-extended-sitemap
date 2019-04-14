# Changelog

## TBA
* fixed `DIRECT_TEMPLATE` usage with `_SAVE_AS` settings [#14]

## 1.2.0
* included the `DIRECT_TEMPLATE` pages into sitemap [#11]

## 1.1.0
* dropped support for Python 3.3
* added support for Python 3.6
* fixed generation for pages without `Date` and `Modified` [#10]

## 1.0.5
* added support for custom `ARTICLE_URL` and `ARTICLE_SAVE_AS` values (thanks to [@wAmpIre](https://github.com/wAmpIre>))

## 1.0.4
* respect ``Modified`` meta value [#8]

## 1.0.3
* fixed failure in sitemap generation if there are no articles [#5]

## 1.0.2
* fixed that if the following settings are not set, no sitemap entry is generated for the appropriate pages
    * `CATEGORY_URL`
    * `TAG_URL`
    * `AUTHOR_URL`

## 1.0.1
* fixed compatibility with Pelican 3.5
* dates are now W3C compliant and do not include time
* adjusted setup.py

## 1.0.0
* fixed wrong package naming, now "extended_sitemap" instead "extended-sitemap"
* added unit tests
* raise ConfigurationError if TIMEZONE setting is not set
* tags are now sorted by name

## 0.2.0
* Python 3 support

## 0.1.4
* fixed date format in sitemap
* changed xml stylesheet link for this package to PyPI

## 0.1.3
* adjusted documentation

## 0.1.2
* adjusted documentation

## 0.1.1
* adjusted documentation

## 0.1.0
* initial release covering index, articles, pages, categories, tags and author pages


[#14]: https://github.com/dArignac/pelican-extended-sitemap/issues/14
[#11]: https://github.com/dArignac/pelican-extended-sitemap/issues/11
[#10]: https://github.com/dArignac/pelican-extended-sitemap/issues/10
[#8]: https://github.com/dArignac/pelican-extended-sitemap/pull/8
[#5]: https://github.com/dArignac/pelican-extended-sitemap/issues/5