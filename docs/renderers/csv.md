---
order: 2
tag: text/csv
---

# CSV

Django REST Pandas' CSV [renderer class][renderers] provides `text/csv` support by calling `to_csv()` on the DataFrame instance.

> To facilitate data API building, the CSV renderer is the default in Django REST Pandas.  While the pandas [JSON renderer][json] is also supported, the primary reason for making CSV the default is the compactness it provides over JSON when serializing time series and other tablular data.

The default CSV output from DRP will have single row of column headers, making it suitable as-is for use with e.g. `d3.csv()`.   However, DRP is often used with the custom serializers below to produce a dataframe with nested multi-row column headers.  This is harder to parse with `d3.csv()` but can be easily processed by [@wq/pandas], an extension to d3.js.

[renderers]: ./index.md
[json]: ./json.md
[@wq/pandas]: ../@wq/pandas.md
