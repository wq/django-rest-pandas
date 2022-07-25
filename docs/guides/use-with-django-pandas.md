# How To: Use With django-pandas

Django REST Pandas includes built-in functionality to [serialize][serializers] querysets into Pandas DataFrames.  However, you can also let [Django Pandas] handle querying and generating the dataframe, and only use Django REST Pandas for the rendering.  To do this, leverage [PandasSimpleView] instead of [PandasView].

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

[serializers]: ../serializers/index.md
[Django Pandas]: https://github.com/chrisdev/django-pandas/
[PandasSimpleView]: ../api/PandasSimpleView.md
[PandasView]: ../api/PandasView.md
