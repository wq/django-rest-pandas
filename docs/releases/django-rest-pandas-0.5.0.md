---
repo: django-rest-pandas
date: 2016-11-08
---

# DRP 0.5.0

Django REST Pandas 0.5.0 introduces a simple `PandasHTMLRenderer` for use in a browseable visualization API (#2).  To enable it by default, you just need to add `rest_pandas` to your `INSTALLED_APPS`.  You will need a template called `rest_pandas.html`, or you can install [django-mustache](https://github.com/wq/django-mustache) to use the provided mustache template (which is optimized for integration with a [wq-powered](https://wq.io/) application).

This release also includes updates for pandas 0.19 and drops support for Django REST Framework 2.4 (#23).
