Django REST Pandas
==================

#### [Django REST Framework] + [Pandas] = A Model-driven Visualization API

This project provides a simple way to generate and serve [Pandas] dataframes via the [Django REST Framework].  The resulting API can serve up JSON and CSV for consumption by a client-side visualization tool like [d3.js].  The actual client implementation is left to the user - giving full flexibility for whatever d3 visualizations you want to come up with.  (That said, if you want some out of the box d3-powered charts, you may be interested in [wq.app]'s [chart.js].)

## Usage

```python
# views.py
from rest_pandas import PandasView
from .models import TimeSeries
class TimeSeriesView(PandasView):
    model = TimeSeries
    def filter_dataframe(self, dataframe):
        return dataframe
```

```python
# urls.py
from django.conf.urls import patterns, include, url
from rest_framework.urlpatterns import format_suffix_patterns

from .views import TimeSeriesView
urlpatterns = patterns('',
    url(r'^data', TimeSeriesView.as_view()),
)
urlpatterns = format_suffix_patterns(urlpatterns)

```


```javascript
// mychart.js
define(['d3'], function(d3) {

d3.csv("/data.csv", render);

function render(error, data) {
    d3.select('svg')
       .selectAll('rect')
       .data(data)
       .enter().append('rect');
    // ...
}

});
```

The default implementation will serve up all of the available data from the provided model in a simple tabular form.  You can also use a `PandasViewSet` if you are using Django REST Framework's ViewSets and Routers, or a `PandasSimpleView` if you would just like to serve up some data without a Django model as the source.

### Implementation
The underlying implementation is a set of [serializers] that take the normal serializer result and put it into a dataframe.  Then, the included [renderers] generate the output using the built in Pandas functionality.  The available formats are CSV, JSON, and Excel (both .xlsx and .xls).

[Django REST Framework]: http://django-rest-framework.org
[Pandas]: http://pandas.pydata.org
[d3.js]: http://d3js.org
[wq.app]: http://wq.io/wq.app
[chart.js]: http://wq.io/docs/chart-js
[serializers]: https://github.com/wq/django-rest-pandas/blob/master/rest_pandas/serializers.py
[renderers]: https://github.com/wq/django-rest-pandas/blob/master/rest_pandas/renderers.py
