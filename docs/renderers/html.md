---
order: 1
tag: text/html
---

# HTML

Django REST Pandas' HTML [renderer class][renderers] provides `text/html` support by calling `to_html()` on the DataFrame class.  The HTML renderer provides the ability to create an interactive view that shares the same URL as your data API.  The dataframe is processed by `to_html()`, then passed to [TemplateHTMLRenderer] with the following context:

context variable | description
-----------------|------------------
`table` | Output `<table>` from `to_html()`
`name` | View name
`description` | View description
`url` | Current URL Path (without parameters)
`url_params` | URL parameters
`available_formats` | Array of allowed extensions (e.g. `'csv'`, `'json'`, `'xlsx'`)
`wq_chart_type` | Recommended chart type (for use with [wq/chartapp.js], see below)

As with `TemplateHTMLRenderer`, the template name is controlled by the view.  If you are using DRP together with the [wq framework], you can leverage the default [mustache/rest_pandas.html] template, which is designed for use with the [wq/chartapp.js][@wq/chart] plugin.  Otherwise, you will probably want to provide a custom template and/or set `template_name` on the view.

If you need to do a lot of customization, and/or you don't really need the entire dataframe rendered in a `<table>`, you can always create another view for the interface and make the `PandasView` only handle the API.

> Note: For backwards compatibility, `PandasHTMLRenderer` is only included in the default `PANDAS_RENDERERS` if `rest_pandas` is listed in your installed apps.

[renderers]: ./index.md
[TemplateHTMLRenderer]: http://www.django-rest-framework.org/api-guide/renderers/#templatehtmlrenderer
[mustache/rest_pandas.html]: https://github.com/wq/django-rest-pandas/blob/master/rest_pandas/mustache/rest_pandas.html
[wq framework]: https://wq.io/
[@wq/chart]: ../@wq/chart.md
