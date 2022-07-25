---
order: 3
tag: text/plain
---

# TXT

Django REST Pandas' TXT [renderer class][renderers] provides `text/plain` support by calling `to_csv()` on the DataFrame instance.  This is the same output as the [CSV renderer][csv], but more useful for manual testing, as most browsers will download a `text/csv` file instead of displaying it.

[renderers]: ./index.md
[csv]: ./csv.md
