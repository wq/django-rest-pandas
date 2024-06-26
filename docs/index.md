---
title: Django REST Pandas
wq_config:
  name: index
  url: ""
  show_in_index: false
---

![Django REST Pandas logo](./images/django-rest-pandas.svg)



#### [Django REST Framework] + [pandas] = A Model-driven Visualization API

**Django REST Pandas** (DRP) provides a simple way to generate and serve [pandas] DataFrames via the [Django REST Framework].  The resulting API can serve up CSV (and a number of [other formats][formats] for consumption by a client-side visualization tool like [@wq/analyst]:

```js
// @wq/analyst
{
    "title": "Live Demo",
    "url": "/weather.csv",
    "initial_rows": 10,
    "initial_order": {
        "date": "desc"
    },
    "formats": {
        "csv": "CSV",
        "xlsx": "Excel",
        "json": "JSON",
        "html": "HTML"
    }
}
```

[**Django REST Pandas on GitHub**](https://github.com/wq/django-rest-pandas)

[pandas]: https://pandas.pydata.org/
[Django REST Framework]: https://www.django-rest-framework.org/
[formats]: ./renderers/index.md
[@wq/analyst]: ./@wq/analyst.md

## News

> This site is under construction.

## Documentation
