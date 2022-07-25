---
order: 5
---

# Custom Integration

If you have an existing viewset, or are otherwise unable to directly subclass one of `PandasSimpleView`, `PandasView`, `PandasViewSet`, or `PandasMixin`, you can also integrate the renderers and serializer directly.  The most important thing is to ensure that your serializer class has `Meta.list_serializer_class` set to `PandasSerializer` or a subclass.  Then, make sure that the Pandas renderers are included in your [renderer options](https://github.com/wq/django-rest-pandas#customizing-renderers).  See [#32] and [#36] for examples.
