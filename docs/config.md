---
wq_config:
   name: config
   url: config
   order: 20
   section: API Reference
   icon_data: M12,15.5A3.5,3.5 0 0,1 8.5,12A3.5,3.5 0 0,1 12,8.5A3.5,3.5 0 0,1 15.5,12A3.5,3.5 0 0,1 12,15.5M19.43,12.97C19.47,12.65 19.5,12.33 19.5,12C19.5,11.67 19.47,11.34 19.43,11L21.54,9.37C21.73,9.22 21.78,8.95 21.66,8.73L19.66,5.27C19.54,5.05 19.27,4.96 19.05,5.05L16.56,6.05C16.04,5.66 15.5,5.32 14.87,5.07L14.5,2.42C14.46,2.18 14.25,2 14,2H10C9.75,2 9.54,2.18 9.5,2.42L9.13,5.07C8.5,5.32 7.96,5.66 7.44,6.05L4.95,5.05C4.73,4.96 4.46,5.05 4.34,5.27L2.34,8.73C2.21,8.95 2.27,9.22 2.46,9.37L4.57,11C4.53,11.34 4.5,11.67 4.5,12C4.5,12.33 4.53,12.65 4.57,12.97L2.46,14.63C2.27,14.78 2.21,15.05 2.34,15.27L4.34,18.73C4.46,18.95 4.73,19.03 4.95,18.95L7.44,17.94C7.96,18.34 8.5,18.68 9.13,18.93L9.5,21.58C9.54,21.82 9.75,22 10,22H14C14.25,22 14.46,21.82 14.5,21.58L14.87,18.93C15.5,18.67 16.04,18.34 16.56,17.94L19.05,18.95C19.27,19.03 19.54,18.95 19.66,18.73L21.66,15.27C21.78,15.05 21.73,14.78 21.54,14.63L19.43,12.97Z
---

# Configuration

### URL Configuration

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

### Customizing Renderers

You can override the [default renderers][renderers] by setting `PANDAS_RENDERERS` in your `settings.py`, or by overriding `renderer_classes` in your individual view(s).  `PANDAS_RENDERERS` is defined separately from Django REST Framework's own `DEFAULT_RENDERER_CLASSES` setting, in case you want to have DRP-enabled views intermingled with regular DRF views.

You can also include DRP renderers in `DEFAULT_RENDERER_CLASSES`.  In that case, extend `PandasMixin` or set `list_serializer_class` on your serializer.  Otherwise, you may get an error saying the serializer output is not a `DataFrame`.  In short, there are three paths to getting DRP renderers working with your views:

 1. Extend [PandasView], [PandasSimpleView], or [PandasViewSet], and use the `PANDAS_RENDERERS` setting (which defaults to the list above).
 2. Extend [PandasMixin] and customize `REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES']` to add one or more `rest_pandas` renderers.
 3. Set `renderer_classes` explicitly on the view, and set `Serializer.Meta.list_serializer_class` to `PandasSerializer` or a subclass.  (See [#32] and [#36] for examples.)

```python
class TimeSeriesView(PandasView):
    # renderer_classes default to PANDAS_RENDERERS
    ...

class TimeSeriesView(PandasMixin, ListAPIView):
    # renderer_classes default to REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES']
    ...
```

### Date Formatting

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

[renderers]: ./renderers/index.md
[#32]: https://github.com/wq/django-rest-pandas/issues/32
[#36]: https://github.com/wq/django-rest-pandas/issues/36
[DateField]: http://www.django-rest-framework.org/api-guide/fields/#datefield
[DateTimeField]: http://www.django-rest-framework.org/api-guide/fields/#datetimefield

