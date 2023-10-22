---
repo: django-rest-pandas
date: 2015-04-20
---

# DRP 0.3.2

This release is just to verify compatibility with Django 1.8 and pandas 0.16.0.  Older versions should still work, though note that Django 1.6 is no longer being tested against.

The only actual code change is https://github.com/wq/django-rest-pandas/commit/5faa4ec4d32466dac89ef117392faa87428a801f, which switches the JSON renderer from a default of `orient="index"` to `orient="records"` <strike>to get around a breaking test</strike> because it's a more reasonable default.  You can restore the old behavior by subclassing `PandasJSONRenderer` and overriding `get_pandas_kwargs()`, but:
1. As is noted in the README, the [CSV renderer](../renderers/csv.md) is the one you probably want to be using anyway.  You can use [wq/pandas.js](../@wq/pandas.md) to convert CSV to JSON after you've loaded it on the client.
2. If you _really_ want JSON output, you're probably already using the vanilla DRF `JSONRenderer` anyway.
