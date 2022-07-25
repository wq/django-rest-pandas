---
order: 4
tag: application/json
---

# JSON

Django REST Pandas' JSON [renderer class][renderers] provides `application/json` support by calling `to_json()` on the DataFrame instance.  [`date_format` and `orient`][to_json] can be provided in URL (e.g. `/path.json?orient=columns`)

> Note that in most cases, DRP's [CSV renderer][csv] is preferred to the JSON renderer due to the compactness a CSV representation provides.

[renderers]: ./index.md
[to_json]: http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.to_json.html
[csv]: ./csv.md
