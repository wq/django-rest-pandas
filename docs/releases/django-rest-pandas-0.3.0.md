---
repo: django-rest-pandas
date: 2015-03-12
---

# DRP 0.3.0

Django REST pandas 0.3.0 adds support for Django REST Framework 3 (#10) and a better separation between model serialization and `DataFrame` creation - the latter now happening in a separate serializer (#8).

The new code is mostly backwards compatible (the tests haven't changed) but there are a couple of implementation changes that may affect you if you've customized or extended DRP.
- `PandasBaseSerializer` has been renamed to `PandasSerializer` and replaces the former `PandasSerializer`.  When using DRP with DRF 3, the new `PandasSerializer` is a [ListSerializer](https://www.django-rest-framework.org/api-guide/serializers/#listserializer) and can only be used as such.
- `PandasSimpleSerializer` has been renamed to `SimpleSerializer` and no longer has any pandas-related functionality (since that's now handled in a separate step).
- For the DRP views, a new `PandasMixin` class encapsulates the functionality needed to add Pandas capabilities to a serialized result.  This is accomplished via the new `with_pandas_serializer(cls)` method that customizes any existing `serializer_class` to enable Pandas capabilities as needed.  The Pandas serializer can be overridden by specifying `pandas_serializer_class`.
