---
wq_config:
    name: serializer
    url: serializers
    order: 21
    section: API Reference
    icon_data: 'M22 15H20V18C20 19.11 19.11 20 18 20H15V22L12 19L15 16V18H18V15H16L19 12L22 15M22 4V8C22 9.1 21.1 10 20 10H10V20C10 21.1 9.1 22 8 22H4C2.9 22 2 21.1 2 20V4C2 2.9 2.9 2 4 2H20C21.1 2 22 2.9 22 4M4 8H8V4H4V8M4 10V14H8V10H4M8 20V16H4V20L8 20M14 8V4H10V8H14M20 4L20 4H16V8H20L20 4Z'
---

# Serializers (DataFrame transformation)

Django REST Pandas provides Django REST Framework serializer classes to create and transform DataFrames.  In addition to the base clase, DRP includes three serializers with `transform_dataframe()` functions that address common use cases.  These serializer classes can be leveraged by assigning them to `pandas_serializer_class` on your view.

These serializers automatically leverage DRP's default [HTML renderer][html] together with [@wq/chart] to provide interactive charts.

[html]: ../renderers/html.md
