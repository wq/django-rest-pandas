Django REST Pandas
==================

#### [Django REST Framework] + [pandas] = A Model-driven Visualization API

**Django REST Pandas** (DRP) provides a simple way to generate and serve [pandas] DataFrames via the [Django REST Framework].  The resulting API can serve up CSV (and a number of [other formats](#supported-formats)) for consumption by a client-side visualization tool like [d3.js].  

The design philosophy of DRP enforces a strict separation between data and presentation.  This keeps the implementation simple, but also has the nice side effect of making it trivial to provide the source data for your visualizations.  This capability can often be leveraged by sending users to the same URL that your visualization code uses internally to load the data.

DRP does not include any JavaScript code, leaving the implementation of interactive visualizations as an exercise for the implementer.  That said, DRP is commonly used in conjunction with the [wq.app] library, which provides [wq/chart.js] and [wq/pandas.js], a collection of chart functions and data loaders that work well with CSV served by DRP.

[![Latest PyPI Release](https://img.shields.io/pypi/v/rest-pandas.svg)](https://pypi.python.org/pypi/rest-pandas)
[![Release Notes](https://img.shields.io/github/release/wq/django-rest-pandas.svg
    )](https://github.com/wq/django-rest-pandas/releases)
[![License](https://img.shields.io/pypi/l/rest-pandas.svg)](https://github.com/wq/django-rest-pandas/blob/master/LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/wq/django-rest-pandas.svg)](https://github.com/wq/django-rest-pandas/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/wq/django-rest-pandas.svg)](https://github.com/wq/django-rest-pandas/network)
[![GitHub Issues](https://img.shields.io/github/issues/wq/django-rest-pandas.svg)](https://github.com/wq/django-rest-pandas/issues)

[![Travis Build Status](https://img.shields.io/travis/wq/django-rest-pandas.svg)](https://travis-ci.org/wq/django-rest-pandas)
[![Python Support](https://img.shields.io/pypi/pyversions/rest-pandas.svg)](https://pypi.org/project/rest-pandas)
[![Django Support](https://img.shields.io/pypi/djversions/rest-pandas.svg)](https://pypi.org/project/rest-pandas)

## Live Demo

The [climata-viewer] project uses Django REST Pandas and [wq/chart.js] to provide interactive visualizations and spreadsheet downloads.

## Related Work
The field of Python-powered data analysis and visualization is growing, and there are a number of similar solutions that may fit your needs better.

 * [Django Pandas] provides a custom ORM model manager with pandas support.  By contrast, Django REST Pandas works at the *view* level, by integrating pandas via custom Django REST Framework serializers and renderers.
 * [DRF-CSV] provides straightforward CSV renderers for use with Django REST Framework.  It may be useful if you just want a CSV API and don't have a need for the pandas DataFrame functionality.
 * [mpld3] provides a direct bridge from [matplotlib] to [d3.js], complete with seamless [IPython] integration.  It is restricted to the (large) matplotlib chart vocabularly but should be sufficient for many use cases.
 * [Bokeh] is a complete client-server visualization platform.  It does not leverage d3 or Django, but is notable as a comprehensive, forward-looking approach to addressing similar use cases.

The goal of Django REST Pandas is to provide a generic REST API for serving up pandas dataframes.  In this sense, it is similar to the Plot Server in Bokeh, but more generic in that it does not assume any particular visualization format or technology.  Further, DRP is optimized for integration with public-facing Django-powered websites (unlike mpld3 which is primarily intended for use within IPython).

In summary, DRP is designed for use cases where:

 * You want to support live spreadsheet downloads as well as interactive visualizations, and/or
 * You want full control over the client visualization stack in order to integrate it with the rest of your website and/or build process.  This usually means writing JavaScript code by hand.  [mpld3] may be a better choice for data exploration if you are more comfortable with (I)Python and need something that can generate interactive visualizations out of the box.

## Supported Formats

The following output formats are provided by default.  These are provided as [renderer classes] in order to leverage the content type negotiation built into Django REST Framework.  This means clients can specify a format via:

 * an HTTP "Accept" header (`Accept: text/csv`),
 * a format parameter (`/path?format=csv`), or
 * a format extension (`/path.csv`)

The HTTP header and format parameter are enabled by default on every pandas view.  Using the extension requires a custom URL configuration (see below).

Format | Content Type | pandas DataFrame Function | Notes
-------|--------------|---------------------------|--------------
HTML   | `text/html` | `to_html()` | See notes on [HTML output](#html-output)
CSV    | `text/csv` | `to_csv()` | &nbsp;
TXT    | `text/plain` | `to_csv()` | Useful for testing, as most browsers will download a CSV file instead of displaying it
JSON   | `application/json` | `to_json()` | [`date_format` and `orient`][to_json] can be provided in URL (e.g. `/path.json?orient=columns`)
XLSX   | `application/vnd.openxml...sheet` | `to_excel()` | &nbsp;
XLS    | `application/vnd.ms-excel` | `to_excel()` | &nbsp;
PNG    | `image/png` | `plot()` | Currently not very customizable, but a simple way to view the data as an image. 
SVG    | `image/svg` | `plot()` | Eventually these could become a fallback for clients that can't handle d3.js

The underlying implementation is a set of [serializers] that take the normal serializer result and put it into a dataframe.  Then, the included [renderers] generate the output using the built in pandas functionality.

## Usage

### Getting Started

```bash
# Recommended: create virtual environment
# python3 -m venv venv
# . venv/bin/activate
pip install rest-pandas
```

**NOTE:** Django REST Pandas relies on pandas, which itself relies on NumPy and other scientific Python libraries written in C.  This is usually fine, since pip can use Python Wheels to install precompiled versions.  If you are having trouble installing DRP due to dependency issues, you may need to pre-install pandas using apt or conda.

### Usage Examples

#### No Model

The example below allows you to create a simple API for an existing Pandas DataFrame, e.g. generated from an existing file.

```python
# views.py
from rest_pandas import PandasSimpleView
import pandas as pd

class TimeSeriesView(PandasSimpleView):
    def get_data(self, request, *args, **kwargs):
        return pd.read_csv('data.csv')
```

#### Model-Backed

The example below assumes you already have a Django project set up with a single `TimeSeries` model.

```python
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

    # Step 5 (Optional).  The default filename may not be particularly useful
    # for your users.  To override, define get_pandas_filename() on your view.
    # If a filename is returned, rest_pandas will include the following header:
    # 'Content-Disposition: attachment; filename="Data Export.xlsx"'
    def get_pandas_filename(self, request, format):
        if format in ('xls', 'xlsx'):
            # Use custom filename and Content-Disposition header
            return "Data Export"  # Extension will be appended automatically
        else:
            # Default filename from URL (no Content-Disposition header)
            return None
```

#### Integrating with Existing Views

If you have an existing viewset, or are otherwise unable to directly subclass one of `PandasSimpleView`, `PandasView`, `PandasViewSet`, or `PandasMixin`, you can also integrate the renderers and serializer directly.  The most important thing is to ensure that your serializer class has `Meta.list_serializer_class` set to `PandasSerializer` or a subclass.  Then, make sure that the Pandas renderers are included in your [renderer options](https://github.com/wq/django-rest-pandas#customizing-renderers).  See [#32] and [#36] for examples.

#### Django Pandas Integration

You can also let [Django Pandas] handle querying and generating the dataframe, and only use Django REST Pandas for the rendering:

```python
# models.py
from django_pandas.managers import DataFrameManager

class TimeSeries(models.Model):
    # ...
    objects = DataFrameManager()

```

```python
# views.py
from rest_pandas import PandasSimpleView
from .models import TimeSeries

class TimeSeriesView(PandasSimpleView):
    def get_data(self, request, *args, **kwargs):
        return TimeSeries.objects.to_timeseries(
            index='date',
        )
```

#### Registering URLs

```python
# urls.py
from django.conf.urls import patterns, include, url

from .views import TimeSeriesView
urlpatterns = patterns('',
    url(r'^data', TimeSeriesView.as_view()),
)

# This is only required to support extension-style formats (e.g. /data.csv)
from rest_framework.urlpatterns import format_suffix_patterns
urlpatterns = format_suffix_patterns(urlpatterns)
```

The default `PandasView` will serve up all of the available data from the provided model in a simple tabular form.  You can also use a `PandasViewSet` if you are using Django REST Framework's [ViewSets] and [Routers].

#### Customizing Renderers

You can override the default renderers by setting `PANDAS_RENDERERS` in your `settings.py`, or by overriding `renderer_classes` in your individual view(s).  `PANDAS_RENDERERS` is defined separately from Django REST Framework's own `DEFAULT_RENDERER_CLASSES` setting, in case you want to have DRP-enabled views intermingled with regular DRF views.

You can also include DRP renderers in `DEFAULT_RENDERER_CLASSES`.  In that case, extend `PandasMixin` or set `list_serializer_class` on your serializer.  Otherwise, you may get an error saying the serializer output is not a `DataFrame`.  In short, there are three paths to getting DRP renderers working with your views:

 1. Extend `PandasView`, `PandasSimpleView`, or `PandasViewSet`, and use the `PANDAS_RENDERERS` setting (which defaults to the list above).
 2. Extend `PandasMixin` and customize `REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES']` to add one or more `rest_pandas` renderers.
 3. Set `renderer_classes` explicitly on the view, and set `Serializer.Meta.list_serializer_class` to `PandasSerializer` or a subclass.  (See [#32] and [#36] for examples.)

```python
class TimeSeriesView(PandasView):
    # renderer_classes default to PANDAS_RENDERERS
    ...

class TimeSeriesView(PandasMixin, ListAPIView):
    # renderer_classes default to REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES']
    ...
```

#### Date Formatting

By default, Django REST Framework will serialize dates as strings before they are processed by the renderer classes.  In many cases, you may want to preserve the dates as `datetime` objects and let Pandas handle the rendering.  To do this, define an explicit [DateTimeField] or [DateField] on your DRF serializer and set `format=None`:

```python
# serializers.py
class TimeSeriesSerializer(serializers.ModelSerializer):
    date = serializers.DateField(format=None)
    class Meta:
        model = TimeSeries
        fields = '__all__'
```

Alternately, you can disable date serialization globally by setting `DATETIME_FORMAT` and/or `DATE_FORMAT` to `None` in your `settings.py`:

```python
# settings.py
DATE_FORMAT = None
```

#### HTML Output

The HTML renderer provides the ability to create an interactive view that shares the same URL as your data API.  The dataframe is processed by `to_html()`, then passed to [TemplateHTMLRenderer] with the following context:

context variable | description
-----------------|------------------
`table` | Output `<table>` from `to_html()`
`name` | View name
`description` | View description
`url` | Current URL Path (without parameters)
`url_params` | URL parameters
`available_formats` | Array of allowed extensions (e.g. `'csv'`, `'json'`, `'xlsx'`)
`wq_chart_type` | Recommended chart type (for use with [wq/chartapp.js], see below)

As with `TemplateHTMLRenderer`, the template name is controlled by the view.  If you are using DRP together with the [wq framework], you can leverage the default [mustache/rest_pandas.html] template, which is designed for use with the [wq/chartapp.js] plugin.  Otherwise, you will probably want to provide a custom template and/or set `template_name` on the view.

If you need to do a lot of customization, and/or you don't really need the entire dataframe rendered in a `<table>`, you can always create another view for the interface and make the `PandasView` only handle the API.

> Note: For backwards compatibility, `PandasHTMLRenderer` is only included in the default `PANDAS_RENDERERS` if `rest_pandas` is listed in your installed apps.

## Building Interactive Charts

In addition to use as a data export tool, DRP is well-suited for creating data API backends for interactive charts.  In particular, DRP can be used with [d3.js], [wq/pandas.js], and [wq/chart.js], to create interactive time series, scatter, and box plot charts - as well as any of the infinite other charting possibilities d3.js provides.

To facilitate data API building, the CSV renderer is the default in Django REST Pandas.  While the pandas JSON serializer is improving, the primary reason for making CSV the default is the compactness it provides over JSON when serializing time series data.  The default CSV output from DRP will have single row of column headers, making it suitable as-is for use with e.g. `d3.csv()`.   However, DRP is often used with the custom serializers below to produce a dataframe with nested multi-row column headers.  This is harder to parse with `d3.csv()` but can be easily processed by [wq/pandas.js], an extension to d3.js.

```javascript
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
```

DRP includes three custom serializers with `transform_dataframe()` functions that address common use cases.  These serializer classes can be leveraged by assigning them to `pandas_serializer_class` on your view.  If you are using the [wq framework], these serializers can automatically leverage DRP's default [HTML template](#html-output) together with [wq/chartapp.js] to provide interactive charts.  If you are not using the full wq framework, you can still use [wq/pandas.js] and [wq/chart.js] directly with the CSV output of these serializers.

For documentation purposes, the examples below assume the following dataset:

 Location | Measurement | Date | Value
---|---|---|---
 site1 | temperature | 2016-01-01 | 3
 site1 | humidity | 2016-01-01 | 30
 site2 | temperature | 2016-01-01 | 4
 site2 | temperature | 2016-01-02 | 5

### PandasUnstackedSerializer
`PandasUnstackedSerializer` [unstacks] the dataframe so a few key attributes are listed in a multi-row column header.  This makes it easier to include metadata about e.g. a time series without repeating the same values on every data row.

To specify which attributes to use in column headers, define the attribute `pandas_unstacked_header` on your `ModelSerializer` subclass.  You will generally also want to define `pandas_index`, which is a list of metadata fields unique to each row (e.g. the timestamp).

```python
# serializers.py
from rest_framework import serializers
from .models import TimeSeries

class TimeSeriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MultiTimeSeries
        fields = ['date', 'location', 'measurement', 'value']
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
```

With the above example data, this configuration would output a CSV file with the following layout:

&nbsp; | Value | Value | Value
---|---|---|---
**Location** | *site1* | *site1* | *site2*
**Measurement** | *temperature* | *humidity* | *temperature*
**Date** | | | &nbsp;
2016-01-01 | 3 | 30 | 4
2016-01-02 | | | 5

This could then be processed by [wq/pandas.js] into the following structure:

```javascript
[
    {
        "location": "site1",
        "measurement": "temperature",
        "data": [
            {"date": "2016-01-01", "value": 3}
        ]
    },
    {
        "location": "site1",
        "measurement": "humidity",
        "data": [
            {"date": "2016-01-01", "value": 30}
        ]
    },
    {
        "location": "site2",
        "measurement": "temperature",
        "data": [
            {"date": "2016-01-01", "value": 4},
            {"date": "2016-01-02", "value": 5}
        ]
    }
]
```

The output of `PandasUnstackedSerializer` can be used with the `timeSeries()` chart provided by [wq/chart.js]:

```javascript
define(['d3', 'wq/pandas', 'wq/chart'], function(d3, pandas, chart) {

var svg = d3.select('svg');
var plot = chart.timeSeries();
pandas.get('/data/timeseries.csv', function(data) {
    svg.datum(data).call(plot);
});

});
```

### PandasScatterSerializer
`PandasScatterSerializer` unstacks the dataframe and also combines selected attributes to make it easier to plot two measurements against each other in an x-y scatterplot.

To specify which attributes to use for the coordinate names, define the attribute `pandas_scatter_coord` on your `ModelSerializer` subclass.  You can also specify additional metadata attributes to include in the header with `pandas_scatter_header`.  You will generally also want to define `pandas_index`, which is a list of metadata fields unique to each row (e.g. the timestamp).

```python
# serializers.py
from rest_framework import serializers
from .models import TimeSeries

class TimeSeriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MultiTimeSeries
        fields = ['date', 'location', 'measurement', 'value']
        pandas_index = ['date']
        pandas_scatter_coord = ['measurement']
        pandas_scatter_header = ['location']

# views.py
from rest_pandas import PandasView, PandasScatterSerializer
from .models import TimeSeries
from .serializers import TimeSeriesSerializer

class TimeSeriesView(PandasView):
    queryset = TimeSeries.objects.all()
    serializer_class = TimeSeriesSerializer
    pandas_serializer_class = PandasScatterSerializer
```

With the above example data, this configuration would output a CSV file with the following layout:

&nbsp; | temperature-value | humidity-value | temperature-value
---|---|---|---
**Location** | *site1* | *site1* | *site2*
**Date** | | | &nbsp;
2014-01-01 | 3 | 30 | 4
2014-01-02 | | | 5

This could then be processed by [wq/pandas.js] into the following structure:

```javascript
[
    {
        "location": "site1",
        "data": [
            {
                "date": "2016-01-01",
                "temperature-value": 3,
                "humidity-value": 30
            }
        ]
    },
    {
        "location": "site2",
        "data": [
            {
                "date": "2016-01-01",
                "temperature-value": 4
            },
            {
                "date": "2016-01-02",
                "temperature-value": 5
            }
        ]
    }
]
```

The output of `PandasScatterSerializer` can be used with the `scatter()` chart provided by [wq/chart.js]:

```javascript
define(['d3', 'wq/pandas', 'wq/chart'], function(d3, pandas, chart) {

var svg = d3.select('svg');
var plot = chart.scatter()
    .xvalue(function(d) {
        return d['temperature-value'];
    })
    .yvalue(function(d) {
        return d['humidity-value'];
    });

pandas.get('/data/scatter.csv', function(data) {
    svg.datum(data).call(plot);
});

});
```

### PandasBoxplotSerializer
`PandasBoxplotSerializer` computes boxplot statistics (via matplotlib's [boxplot_stats]) and pushes the results out via an unstacked dataframe.  The statistics can be aggregated for a specified group column as well as by date.

To specify which attribute to use for the group column, define the attribute `pandas_boxplot_group` on your `ModelSerializer` subclass.  To specify an attribute to use for date-based grouping, define `pandas_boxplot_date`.   You will generally also want to define `pandas_boxplot_header`, which will unstack any metadata columns and exclude them from statistics.

```python
# serializers.py
from rest_framework import serializers
from .models import TimeSeries

class TimeSeriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MultiTimeSeries
        fields = ['date', 'location', 'measurement', 'value']
        pandas_boxplot_group = 'site'
        pandas_boxplot_date = 'date'
        pandas_boxplot_header = ['measurement']

# views.py
from rest_pandas import PandasView, PandasBoxplotSerializer
from .models import TimeSeries
from .serializers import TimeSeriesSerializer

class TimeSeriesView(PandasView):
    queryset = TimeSeries.objects.all()
    serializer_class = TimeSeriesSerializer
    pandas_serializer_class = PandasBoxplotSerializer
```

With the above example data, this configuration will output a CSV file with the same general structure as `PandasUnstackedSerializer`, but with the `value` spread across multiple boxplot statistics columns (`value-mean`, `value-q1`,value-whishi`, etc.).  An optional `group` parameter can be added to the query string to switch between various groupings:

name | purpose
-----|---------
`?group=series` | Group by series (`pandas_boxplot_group`)
`?group=series-year` | Group by series, then by year
`?group=series-month` | Group by series, then by month
`?group=year` | Summarize all data by year
`?group=month` | Summarize all data by month

The output of `PandasBoxplotSerializer` can be used with the `boxplot()` chart provided by [wq/chart.js]:

```javascript
define(['d3', 'wq/pandas', 'wq/chart'], function(d3, pandas, chart) {

var svg = d3.select('svg');
var plot = chart.boxplot();
pandas.get('/data/boxplot.csv?group=year', function(data) {
    svg.datum(data).call(plot);
});

});
```

[Django REST Framework]: http://django-rest-framework.org
[pandas]: http://pandas.pydata.org
[d3.js]: http://d3js.org
[wq.app]: https://wq.io/wq.app
[wq/chart.js]: https://wq.io/docs/chart-js
[wq.db]: https://wq.io/wq.db
[chart]: https://wq.io/docs/chart
[climata-viewer]: http://climata.houstoneng.net
[Django Pandas]: https://github.com/chrisdev/django-pandas/
[bokeh]: http://bokeh.pydata.org/
[mpld3]: http://mpld3.github.io/
[DRF-CSV]: https://github.com/mjumbewu/django-rest-framework-csv
[matplotlib]: http://matplotlib.org/
[IPython]: http://ipython.org/
[renderer classes]: http://www.django-rest-framework.org/api-guide/renderers
[ViewSets]: http://www.django-rest-framework.org/api-guide/viewsets
[Routers]: http://www.django-rest-framework.org/api-guide/routers
[DateField]: http://www.django-rest-framework.org/api-guide/fields/#datefield
[DateTimeField]: http://www.django-rest-framework.org/api-guide/fields/#datetimefield
[serializers]: https://github.com/wq/django-rest-pandas/blob/master/rest_pandas/serializers.py
[renderers]: https://github.com/wq/django-rest-pandas/blob/master/rest_pandas/renderers.py
[TemplateHTMLRenderer]: http://www.django-rest-framework.org/api-guide/renderers/#templatehtmlrenderer
[wq framework]: https://wq.io/
[wq/chartapp.js]: https://wq.io/docs/chartapp-js
[wq/pandas.js]: https://wq.io/docs/pandas-js
[mustache/rest_pandas.html]: https://github.com/wq/django-rest-pandas/blob/master/rest_pandas/mustache/rest_pandas.html
[to_json]: http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.to_json.html
[unstacks]: http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.unstack.html
[boxplot_stats]: http://matplotlib.org/api/cbook_api.html#matplotlib.cbook.boxplot_stats
[#32]: https://github.com/wq/django-rest-pandas/issues/32
[#36]: https://github.com/wq/django-rest-pandas/issues/36
