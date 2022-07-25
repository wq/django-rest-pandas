---
order: 4
---

# PandasBoxplotSerializer

Django REST Pandas' `PandasBoxplotSerializer` [serializer class][serializers] extends [PandasSerializer] to compute statistics for generating box-and-whisker plots.

`PandasBoxplotSerializer` computes boxplot statistics via matplotlib's [boxplot_stats] and pushes the results out via an unstacked dataframe.  The statistics can be aggregated for a specified group column as well as by date.

To specify which attribute to use for the group column, define the attribute `pandas_boxplot_group` on your `ModelSerializer` subclass.  To specify an attribute to use for date-based grouping, define `pandas_boxplot_date`.   You will generally also want to define `pandas_boxplot_header`, which will unstack any metadata columns and exclude them from statistics.

The example below assumes the following dataset:

 Location | Measurement | Date | Value
---|---|---|---
 site1 | temperature | 2016-01-01 | 3
 site1 | humidity | 2016-01-01 | 30
 site2 | temperature | 2016-01-01 | 4
 site2 | temperature | 2016-01-02 | 5

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

The output of `PandasBoxplotSerializer` can be used with the `boxplot()` chart provided by [@wq/chart]:

```javascript
define(['d3', 'wq/pandas', 'wq/chart'], function(d3, pandas, chart) {

var svg = d3.select('svg');
var plot = chart.boxplot();
pandas.get('/data/boxplot.csv?group=year', function(data) {
    svg.datum(data).call(plot);
});

});
```

[serializers]: ./index.md
[PandasSerializer]: ./PandasSerializer.md
[boxplot_stats]: http://matplotlib.org/api/cbook_api.html#matplotlib.cbook.boxplot_stats
[@wq/pandas]: ../@wq/pandas.md
[@wq/chart]: ../@wq/chart.md
