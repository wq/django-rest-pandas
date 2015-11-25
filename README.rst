Django REST Pandas
==================

*Django REST Framework + pandas = A Model-driven Visualization API*

**Django REST Pandas** (DRP) provides a simple way to generate and serve
`pandas <http://pandas.pydata.org>`__ DataFrames via the `Django REST
Framework <http://django-rest-framework.org>`__. The resulting API can
serve up CSV (and a number of other formats)
for consumption by a client-side visualization tool like
`d3.js <http://d3js.org>`__.

The design philosophy of DRP enforces a strict separation between data
and presentation. This keeps the implementation simple, but also has the
nice side effect of making it trivial to provide the source data for
your visualizations. This capability can often be leveraged by sending
users to the same URL that your visualization code uses internally to
load the data.

DRP does not include any JavaScript code, leaving the implementation of
interactive visualizations as an exercise for the implementer. That
said, DRP is commonly used in conjunction with the
`wq.app <http://wq.io/wq.app>`__ library, which provides
`wq/chart.js <http://wq.io/docs/chart-js>`__ and
`wq/pandas.js <http://wq.io/docs/pandas-js>`__, a collection of chart
functions and data loaders that work well with CSV served by DRP and
`wq.db <http://wq.io/wq.db>`__'s `chart <http://wq.io/docs/chart>`__
module.

|Latest PyPI Release| |Release Notes| |License| |GitHub Stars| |GitHub
Forks| |GitHub Issues|

|Travis Build Status| |Python Support| |Django Support| |Django REST
Framework Support|

**Note:** Support for Django REST Framework 2.4 will be dropped in DRP
0.5.

Live Demo
---------

The `climata-viewer <http://climata.houstoneng.net>`__ project uses
Django REST Pandas and `wq/chart.js <http://wq.io/docs/chart-js>`__ to
provide interactive visualizations and spreadsheet downloads.

Related Work
------------

The field of Python-powered data analysis and visualization is growing,
and there are a number of similar solutions that may fit your needs
better.

-  `Django Pandas <https://github.com/chrisdev/django-pandas/>`__
   provides a custom ORM model manager with pandas support. By contrast,
   Django REST Pandas works at the *view* level, by integrating pandas
   via custom Django REST Framework serializers and renderers.
-  `DRF-CSV <https://github.com/mjumbewu/django-rest-framework-csv>`__
   provides straightforward CSV renderers for use with Django REST
   Framework. It may be useful if you just want a CSV API and don't have
   a need for the pandas DataFrame functionality.
-  `mpld3 <http://mpld3.github.io/>`__ provides a direct bridge from
   `matplotlib <http://matplotlib.org/>`__ to
   `d3.js <http://d3js.org>`__, complete with seamless
   `IPython <http://ipython.org/>`__ integration. It is restricted to
   the (large) matplotlib chart vocabularly but should be sufficient for
   many use cases.
-  `Bokeh <http://bokeh.pydata.org/>`__ is a complete client-server
   visualization platform. It does not leverage d3 or Django, but is
   notable as a comprehensive, forward-looking approach to addressing
   similar use cases.

The goal of Django REST Pandas is to provide a generic REST API for
serving up pandas dataframes. In this sense, it is similar to the Plot
Server in Bokeh, but more generic in that it does not assume any
particular visualization format or technology. Further, DRP is optimized
for integration with public-facing Django-powered websites (unlike mpld3
which is primarily intended for use within IPython).

In summary, DRP is designed for use cases where:

-  You want to support live spreadsheet downloads as well as interactive
   visualizations, and/or
-  You want full control over the client visualization stack in order to
   integrate it with the rest of your website and/or build process. This
   usually means writing JavaScript code by hand.
   `mpld3 <http://mpld3.github.io/>`__ may be a better choice for data
   exploration if you are more comfortable with (I)Python and need
   something that can generate interactive visualizations out of the
   box.

Supported Formats
-----------------

The following output formats are provided by default. These are provided
as `renderer
classes <http://www.django-rest-framework.org/api-guide/renderers>`__ in
order to leverage the content type negotiation built into Django REST
Framework. This means clients can specify a format via:

-  an HTTP "Accepts" header (``Accepts: text/csv``),
-  a format parameter (``/path?format=csv``), or
-  a format extension (``/path.csv``)

The HTTP header and format parameter are enabled by default on every
pandas view. Using the extension requires a custom URL configuration
(see below).

.. csv-table::
  :header: "Format", "Content Type", "pandas Dataframe Function", "Notes"
  :widths: 50, 150, 70, 500

  CSV,``text/csv``,``to_csv()``,
  TXT,``text/plain``,``to_csv()``,"Useful for testing, as most browsers will download a CSV file instead of displaying it"
  JSON,``application/json``,``to_json()``,
  XLSX,``application/vnd.openxml...sheet``,``to_excel()``,
  XLS,``application/vnd.ms-excel``,``to_excel()``,
  PNG,``image/png``,``plot()``,"Currently not very customizable, but a simple way to view the data as an image."
  SVG,``image/svg``,``plot()``,"Eventually these could become a fallback for clients that can't handle d3.js"

The underlying implementation is a set of
`serializers <https://github.com/wq/django-rest-pandas/blob/master/rest_pandas/serializers.py>`__
that take the normal serializer result and put it into a dataframe.
Then, the included
`renderers <https://github.com/wq/django-rest-pandas/blob/master/rest_pandas/renderers.py>`__
generate the output using the built in pandas functionality.

Usage
-----

Getting Started
~~~~~~~~~~~~~~~

.. code:: bash

    pip3 install rest-pandas

**NOTE:** Django REST Pandas relies on pandas, which itself relies on
NumPy and other scientific Python libraries. If you are having trouble
installing DRP due to dependency issues, you may want to pre-install
Pandas using another tool. For example, on Ubuntu 14.04 LTS you can
pre-install pandas using this command:

.. code:: bash

    sudo apt-get install python3-pandas
    sudo pip3 install rest-pandas

The `pandas documentation <http://pandas.pydata.org>`__ recommends using
conda to install pandas for similar reasons. We've found the apt-get
approach to be the fastest route to getting DRP running with the default
Apache WSGI implementation on Ubuntu.

Usage Example
~~~~~~~~~~~~~

No Model
^^^^^^^^

The example below allows you to create a simple API for an existing
Pandas DataFrame, e.g. generated from an existing file.

.. code:: python

    # views.py
    from rest_pandas import PandasSimpleView
    import pandas as pd


    class TimeSeriesView(PandasSimpleView):
        def get_data(self):
            return pd.read_csv('data.csv')

Model-Backed
^^^^^^^^^^^^

The example below assumes you already have a Django project set up with
a single ``TimeSeries`` model.

.. code:: python

    # views.py
    from rest_pandas import PandasView
    from .models import TimeSeries
    from .serializers import TimeSeriesSerializer

    # Short version (leverages default DRP settings):
    class TimeSeriesView(PandasView):
        queryset = TimeSeries.objects.all()
        serializer_class = TimeSeriesSerializer
        # That's it!  The view will be able to export the model dataset to any of
        # the included formats listed above.  No further customization is needed to
        # leverage the defaults.

    # Long Version and step-by-step explanation
    class TimeSeriesView(PandasView):
        # Assign a default model queryset to the view
        queryset = TimeSeries.objects.all()

        # Step 1. In response to get(), the underlying Django REST Framework view
        # will load the queryset and then pass it to the following function.
        def filter_queryset(self, qs): 
            # At this point, you can filter queryset based on self.request or other
            # settings (useful for limiting memory usage).  This function can be
            # omitted if you are using a filter backend or do not need filtering.
            return qs
            
        # Step 2. A Django REST Framework serializer class should serialize each
        # row in the queryset into a simple dict format.  A simple ModelSerializer
        # should be sufficient for most cases.
        serializer_class = TimeSeriesSerializer  # extends ModelSerializer

        # Step 3.  The included PandasSerializer will load all of the row dicts
        # into array and convert the array into a pandas DataFrame.  The DataFrame
        # is essentially an intermediate format between Step 2 (dict) and Step 4
        # (output format).  The default DataFrame simply maps each model field to a
        # column heading, and will be sufficient in many cases.  If you do not need
        # to transform the dataframe, you can skip to step 4.
        
        # If you would like to transform the dataframe (e.g. to pivot or add
        # columns), you can do so in one of two ways:

        # A. Create a subclass of PandasSerializer, define a function called
        # transform_dataframe(self, dataframe) on the subclass, and assign it to
        # pandas_serializer_class on the view.  You can also use one of the three
        # provided pivoting serializers (see Advanced Usage below).
        #
        # class MyCustomPandasSerializer(PandasSerializer):
        #     def transform_dataframe(self, dataframe):
        #         dataframe.some_pivot_function(in_place=True)
        #         return dataframe
        #
        pandas_serializer_class = MyCustomPandasSerializer

        # B. Alternatively, you can create a custom transform_dataframe function
        # directly on the view.  Again, if no custom transformations are needed,
        # this function does not need to be defined.
        def transform_dataframe(self, dataframe):
            dataframe.some_pivot_function(in_place=True)
            return dataframe
        
        # NOTE: As the name implies, the primary purpose of transform_dataframe()
        # is to apply a transformation to an existing dataframe.  In PandasView,
        # this dataframe is created by serializing data queried from a Django
        # model.  If you would like to supply your own custom DataFrame from the
        # start (without using a Django model), you can do so with PandasSimpleView
        # as shown in the first example.

        # Step 4. Finally, the provided renderer classes will convert the DataFrame
        # to any of the supported output formats (see above).  By default, all of
        # the formats above are enabled.  To restrict output to only the formats
        # you are interested in, you can define renderer_classes on the view:
        renderer_classes = [PandasCSVRenderer, PandasExcelRenderer]
        # You can also set the default renderers for all of your pandas views by
        # defining the PANDAS_RENDERERS in your settings.py.

Registering URLs
^^^^^^^^^^^^^^^^

.. code:: python

    # urls.py
    from django.conf.urls import patterns, include, url

    from .views import TimeSeriesView
    urlpatterns = patterns('',
        url(r'^data', TimeSeriesView.as_view()),
    )

    # This is only required to support extension-style formats (e.g. /data.csv)
    from rest_framework.urlpatterns import format_suffix_patterns
    urlpatterns = format_suffix_patterns(urlpatterns)

The default ``PandasView`` will serve up all of the available data from
the provided model in a simple tabular form. You can also use a
``PandasViewSet`` if you are using Django REST Framework's
`ViewSets <http://www.django-rest-framework.org/api-guide/viewsets>`__
and
`Routers <http://www.django-rest-framework.org/api-guide/routers>`__.

Building Interactive Charts with DRP and d3.js
----------------------------------------------

In addition to use as a data export tool, DRP is well-suited for
creating data API backends for interactive charts. In particular, DRP
can be used with `d3.js <http://d3js.org>`__,
`wq/pandas.js <http://wq.io/docs/pandas-js>`__, and
`wq/chart.js <http://wq.io/docs/chart-js>`__, to create interactive time
series, scatter, and box plot charts - as well as any of the infinite
other charting possibilities d3.js provides.

To facilitate data API building, the CSV renderer is the default in
Django REST Pandas. While the pandas JSON serializer is improving, the
primary reason for making CSV the default is the compactness it provides
over JSON when serializing time series data. The default CSV output from
DRP will have single row of column headers, making it suitable as-is for
use with e.g. d3.csv(). However, DRP is often used with the custom
serializers below to produce a dataframe with nested multi-row column
headers. This is harder to parse with ``d3.csv()`` but can be easily
processed by `wq/pandas.js <http://wq.io/docs/pandas-js>`__, an
extension to d3.js.

.. code:: javascript

    // mychart.js
    define(['d3', 'wq/pandas', 'wq/chart'], function(d3, pandas, chart) {

    // Unpivoted data (single-row header)
    d3.csv("/data.csv", render);

    // Pivoted data (multi-row header)
    pandas.get('/data.csv', render);

    function render(error, data) {
        d3.select('svg')
           .selectAll('rect')
           .data(data)
           // ...
    }

    });

You can override the default renderers by setting ``PANDAS_RENDERERS``
in your ``settings.py``, or by overriding ``renderer_classes`` in your
``PandasView`` subclass. ``PANDAS_RENDERERS`` is intentionally set
separately from Django REST Framework's own ``DEFAULT_RENDERER_CLASSES``
setting, as it is likely that you will be mixing DRP views with regular
DRF views.

As of version 0.4, DRP includes three custom serializers with
``transform_dataframe()`` functions that address common use cases. These
serializer classes can be leveraged by assigning them to
``pandas_serializer_class`` on your view.

For documentation purposes, the examples below assume the following
dataset:

+------------+---------------+--------------+---------+
| Location   | Measurement   | Date         | Value   |
+============+===============+==============+=========+
| site1      | temperature   | 2016-01-01   | 3       |
+------------+---------------+--------------+---------+
| site1      | humidity      | 2016-01-01   | 30      |
+------------+---------------+--------------+---------+
| site2      | temperature   | 2016-01-01   | 4       |
+------------+---------------+--------------+---------+
| site2      | temperature   | 2016-01-02   | 5       |
+------------+---------------+--------------+---------+

PandasUnstackedSerializer
~~~~~~~~~~~~~~~~~~~~~~~~~

``PandasUnstackedSerializer``
`unstacks <http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.unstack.html>`__
the dataframe so a few key attributes are listed in a multi-row column
header. This makes it easier to include metadata about e.g. a time
series without repeating the same values on every data row.

To specify which attributes to use in column headers, define the
attribute ``pandas_unstacked_header`` on your ``ModelSerializer``
subclass. This header would usually contain information that
distinguiYou will generally also want to define ``pandas_index``, which
is a list of metadata fields unique to each row (e.g. the timestamp).

.. code:: python

    # serializers.py
    from rest_framework import serializers
    from .models import TimeSeries

    class TimeSeriesSerializer(ModelSerializer):
        class Meta:
            model = MultiTimeSeries
            pandas_index = ['date']
            pandas_unstacked_header = ['location', 'measurement']

    # views.py
    from rest_pandas import PandasView, PandasUnstackedSerializer
    from .models import TimeSeries
    from .serializers import TimeSeriesSerializer

    class TimeSeriesView(PandasView):
        queryset = TimeSeries.objects.all()
        serializer_class = TimeSeriesSerializer
        pandas_serializer_class = PandasUnstackedSerializer

With the above example data, this configuration would output a CSV file
with the following layout:

+-------------------+---------------+------------+---------------+
|                   | Value         | Value      |
+===================+===============+============+===============+
| **Location**      | site1         | site1      | site2         |
+-------------------+---------------+------------+---------------+
| **Measurement**   | temperature   | humidity   | temperature   |
+-------------------+---------------+------------+---------------+
| **Date**          |               |            |
+-------------------+---------------+------------+---------------+
| 2014-01-01        | 3             | 30         | 4             |
+-------------------+---------------+------------+---------------+
| 2014-01-02        |               |            | 5             |
+-------------------+---------------+------------+---------------+

The output of ``PandasUnstackedSerializer`` can be used with the
``timeSeries()`` chart provided by
`wq/chart.js <http://wq.io/docs/chart-js>`__:

.. code:: javascript

    define(['d3', 'wq/pandas', 'wq/chart'], function(d3, pandas, chart) {

    var svg = d3.select('svg');
    var plot = chart.timeSeries();
    pandas.get('/data/timeseries.csv', function(data) {
        svg.datum(data).call(plot);
    });

    });

PandasScatterSerializer
~~~~~~~~~~~~~~~~~~~~~~~

FIXME: add details

PandasBoxplotSerializer
~~~~~~~~~~~~~~~~~~~~~~~

FIXME: add details

.. |Latest PyPI Release| image:: https://img.shields.io/pypi/v/rest-pandas.svg
   :target: https://pypi.python.org/pypi/rest-pandas
.. |Release Notes| image:: https://img.shields.io/github/release/wq/django-rest-pandas.svg
   :target: https://github.com/wq/django-rest-pandas/releases
.. |License| image:: https://img.shields.io/pypi/l/rest-pandas.svg
   :target: https://github.com/wq/django-rest-pandas/blob/master/LICENSE
.. |GitHub Stars| image:: https://img.shields.io/github/stars/wq/django-rest-pandas.svg
   :target: https://github.com/wq/django-rest-pandas/stargazers
.. |GitHub Forks| image:: https://img.shields.io/github/forks/wq/django-rest-pandas.svg
   :target: https://github.com/wq/django-rest-pandas/network
.. |GitHub Issues| image:: https://img.shields.io/github/issues/wq/django-rest-pandas.svg
   :target: https://github.com/wq/django-rest-pandas/issues
.. |Travis Build Status| image:: https://img.shields.io/travis/wq/django-rest-pandas.svg
   :target: https://travis-ci.org/wq/django-rest-pandas
.. |Python Support| image:: https://img.shields.io/pypi/pyversions/rest-pandas.svg
   :target: https://pypi.python.org/pypi/rest-pandas
.. |Django Support| image:: https://img.shields.io/badge/Django-1.7%2C%201.8-blue.svg
   :target: https://pypi.python.org/pypi/rest-pandas
.. |Django REST Framework Support| image:: https://img.shields.io/badge/DRF-2.4%2C%203.3-blue.svg
   :target: https://pypi.python.org/pypi/rest-pandas
