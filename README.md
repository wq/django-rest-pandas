<p align="center">
  <a href="https://django-rest-pandas.wq.io">
    <img src="https://django-rest-pandas.wq.io/images/django-rest-pandas.svg" alt="Django REST Pandas">
  </a>
</p>

#### [Django REST Framework] + [pandas] = A Model-driven Visualization API

**Django REST Pandas** (DRP) provides a simple way to generate and serve [pandas] DataFrames via the [Django REST Framework].  The resulting API can serve up CSV (and a number of [other formats][renderers] for consumption by a client-side visualization tool like [@wq/analyst].

The design philosophy of DRP enforces a strict separation between data and presentation.  This keeps the implementation simple, but also has the nice side effect of making it trivial to provide the source data for your visualizations.  This capability can often be leveraged by sending users to the same URL that your visualization code uses internally to load the data.

While DRP is primarily a data API, it also provides a default collection of interactive visualizations through the [@wq/chart] library, and a [@wq/pandas] loader to facilitate custom JavaScript charts that work well with CSV output served by DRP.  These can be used to create interactive time series, scatter, and box plot charts - as well as any of the other charting possibilities Plotly provides.

[![Latest PyPI Release](https://img.shields.io/pypi/v/rest-pandas.svg)](https://pypi.python.org/pypi/rest-pandas)
[![Release Notes](https://img.shields.io/github/release/wq/django-rest-pandas.svg
    )](https://github.com/wq/django-rest-pandas/releases)
[![License](https://img.shields.io/pypi/l/rest-pandas.svg)](https://github.com/wq/django-rest-pandas/blob/master/LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/wq/django-rest-pandas.svg)](https://github.com/wq/django-rest-pandas/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/wq/django-rest-pandas.svg)](https://github.com/wq/django-rest-pandas/network)
[![GitHub Issues](https://img.shields.io/github/issues/wq/django-rest-pandas.svg)](https://github.com/wq/django-rest-pandas/issues)

[![Tests](https://github.com/wq/django-rest-pandas/actions/workflows/test.yml/badge.svg)](https://github.com/wq/django-rest-pandas/actions/workflows/test.yml)
[![Python Support](https://img.shields.io/pypi/pyversions/rest-pandas.svg)](https://pypi.org/project/rest-pandas)
[![Django Support](https://img.shields.io/pypi/djversions/rest-pandas.svg)](https://pypi.org/project/rest-pandas)


### [Documentation]

DRP is configured by defining one or more [API views][api] and mapping them to URLs.  The underlying implementation is a set of [serializers] that take Django REST Framework's serializer output and converts it into a dataframe.  Then, the included [renderers] generate the output file using pandas' built in functionality.

1. **Getting Started**
   * [Installation][installation]
   * [Related Work][related-work]

2. **API Documentation**
   * [Configuration][config]
   * [API Views][api]
   * [Serializers (DataFrame transformation)][serializers]
   * [Renderers (Output Formats)][renderers]

3. **Data Visualization**
   * [@wq/analyst]
   * [@wq/chart]
   * [@wq/pandas]

[Django REST Framework]: http://django-rest-framework.org
[pandas]: http://pandas.pydata.org
[Plotly]: https://plotly.com/javascript/
[Documentation]: https://django-rest-pandas.wq.io/
[installation]: https://django-rest-pandas.wq.io/overview/setup
[related-work]: https://django-rest-pandas.wq.io/overview/related-work
[config]: https://django-rest-pandas.wq.io/config
[api]: https://django-rest-pandas.wq.io/api/
[serializers]: https://django-rest-pandas.wq.io/serializers/
[renderers]: https://django-rest-pandas.wq.io/renderers/
[@wq/pandas]: https://django-rest-pandas.wq.io/@wq/pandas
[@wq/chart]: https://django-rest-pandas.wq.io/@wq/chart
[@wq/analyst]: https://django-rest-pandas.wq.io/@wq/analyst
