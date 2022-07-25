# Related Work

The field of Python-powered data analysis and visualization is growing, and there are a number of similar solutions that may fit your needs better.

 * [Django Pandas] provides a custom ORM model manager with pandas support.  By contrast, Django REST Pandas works at the *view* level, by integrating pandas via custom Django REST Framework serializers and renderers.
 * [DRF-CSV] provides straightforward CSV renderers for use with Django REST Framework.  It may be useful if you just want a CSV API and don't have a need for the pandas DataFrame functionality.
 * [mpld3] provides a direct bridge from [matplotlib] to [d3.js], complete with seamless [IPython] integration.  It is restricted to the (large) matplotlib chart vocabularly but should be sufficient for many use cases.
 * [Bokeh] is a complete client-server visualization platform.  It does not leverage d3 or Django, but is notable as a comprehensive, forward-looking approach to addressing similar use cases.

The goal of Django REST Pandas is to provide a generic REST API for serving up pandas dataframes.  In this sense, it is similar to the Plot Server in Bokeh, but more generic in that it does not assume any particular visualization format or technology.  Further, DRP is optimized for integration with public-facing Django-powered websites (unlike mpld3 which is primarily intended for use within IPython).

In summary, DRP is designed for use cases where:

 * You want to support live spreadsheet downloads as well as interactive visualizations, and/or
 * You want full control over the client visualization stack in order to integrate it with the rest of your website and/or build process.  This usually means writing JavaScript code by hand.  [mpld3] may be a better choice for data exploration if you are more comfortable with (I)Python and need something that can generate interactive visualizations out of the box.

[Django Pandas]: https://github.com/chrisdev/django-pandas/
[DRF-CSV]: https://github.com/mjumbewu/django-rest-framework-csv
[mpld3]: http://mpld3.github.io/
[matplotlib]: http://matplotlib.org/
[d3.js]: http://d3js.org
[IPython]: http://ipython.org/
[bokeh]: http://bokeh.pydata.org/
