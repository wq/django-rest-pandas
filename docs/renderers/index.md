---
wq_config:
    name: renderer
    url: renderers
    order: 23
    section: API Reference
    icon_data: 'M14 2H6C4.9 2 4 2.9 4 4V20C4 21.1 4.9 22 6 22H18C19.1 22 20 21.1 20 20V8L14 2M18 20H6V4H13V9H18V20M10 19L12 15H9V10H15V15L13 19H10'
---

# Renderers (Output Formats)

Django REST Pandas provides the following output formats by default.  These are provided as [renderer classes] in order to leverage the content type negotiation built into Django REST Framework.  This means clients can specify a format via:

 * an HTTP "Accept" header (`Accept: text/csv`),
 * a format parameter (`/path?format=csv`), or
 * a format extension (`/path.csv`)

The HTTP header and format parameter are enabled by default on every pandas view.  Using the extension requires a custom [URL configuration][config].

The default render classes can be extended or overridden by specifying [PANDAS_RENDERERS][config] in your Django settings.

[renderer classes]: http://www.django-rest-framework.org/api-guide/renderers
[config]: ../config.md
