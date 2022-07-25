---
order: 1
---

# PandasSimpleView (No Model)

Django REST Pandas' `PandasSimpleView` [view class][views] allows you to create a simple API for an existing Pandas DataFrame, e.g. generated from an existing file.

```python
# views.py
from rest_pandas import PandasSimpleView
import pandas as pd

class TimeSeriesView(PandasSimpleView):
    def get_data(self, request, *args, **kwargs):
        return pd.read_csv('data.csv')
```

[views]: ./index.md
