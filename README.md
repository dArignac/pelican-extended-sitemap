## pelican-extended-sitemap

A sitemap plugin for [Pelican](https://github.com/getpelican/pelican).

It generates a sitemap.xml according to the specification of [sitemaps.org](http://sitemaps.org) and considers the pelican index page, articles, pages and special pages (like tags, categories, authors).
Also comes with a XML stylesheet to be able to view the sitemap in browser without pain.

**ATTENTION: Plugin is in heavy development - do not use yet!**

### ToDos

What still has to be implemented:

* make a real python package
* i18n (maybe)


### Pelican settings

Add to the plugins list:


```python
PLUGINS = [
    'plugins.extended-sitemap'
]
```

### Plugin settings

Add the `EXTENDED_SITEMAP_PLUGIN` dict to your settings.
The keys explained:

* priorities: priority for each page type, from 0.0 to 1.0
 * index: index page
 * articles: article pages
 * pages: pages
 * others: category, tags and authors pages
* changefrequencies: how often a page will likely change, possible values: always, hourly, daily, weekly, monthly, yearly, never

The settings below are the default values:

```python
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
```
