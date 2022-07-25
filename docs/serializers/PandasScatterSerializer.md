---
order: 3
---

# PandasScatterSerializer

Django REST Pandas' `PandasUnstackedSerializer` [serializer class][serializers] extends [PandasSerializer] to [unstack] the dataframe and combine selected attributes to make it easier to plot two measurements against each other in an x-y scatterplot.

To specify which attributes to use for the coordinate names, define the attribute `pandas_scatter_coord` on your `ModelSerializer` subclass.  You can also specify additional metadata attributes to include in the header with `pandas_scatter_header`.  You will generally also want to define `pandas_index`, which is a list of metadata fields unique to each row (e.g. the timestamp).

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

This could then be processed by [@wq/pandas] into the following structure:

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

The output of `PandasScatterSerializer` can be used with the `scatter()` chart provided by [@wq/chart]:

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

[serializers]: ./index.md
[PandasSerializer]: ./PandasSerializer.md
[unstack]: http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.unstack.html
[@wq/pandas]: ../@wq/pandas.md
[@wq/chart]: ../@wq/chart.md
