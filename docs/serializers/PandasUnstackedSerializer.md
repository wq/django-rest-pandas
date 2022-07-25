---
order: 2
---

# PandasUnstackedSerializer

Django REST Pandas' `PandasUnstackedSerializer` [serializer class][serializers] extends [PandasSerializer] to pivot repeating series metadata to the top of the dataframe.

To do this, `PandasUnstackedSerializer` [unstacks] the dataframe so a few key attributes are listed in a multi-row column header.  This makes it easier to include metadata about e.g. a time series without repeating the same values on every data row.

To specify which attributes to use in column headers, define the attribute `pandas_unstacked_header` on your `ModelSerializer` subclass.  You will generally also want to define `pandas_index`, which is a list of metadata fields unique to each row (e.g. the timestamp).

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

This could then be processed by [@wq/pandas] into the following structure:

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

The output of `PandasUnstackedSerializer` can be used with the `timeSeries()` chart provided by [@wq/chart]:

```javascript
define(['d3', 'wq/pandas', 'wq/chart'], function(d3, pandas, chart) {

var svg = d3.select('svg');
var plot = chart.timeSeries();
pandas.get('/data/timeseries.csv', function(data) {
    svg.datum(data).call(plot);
});

});
```

[serializers]: ./index.md
[PandasSerializer]: ./PandasSerializer.md
[unstacks]: http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.unstack.html
[@wq/pandas]: ../@wq/pandas.md
[@wq/chart]: ../@wq/chart.md
