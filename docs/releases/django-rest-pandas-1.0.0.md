---
repo: django-rest-pandas
date: 2017-09-13
---

# DRP 1.0.0

Django REST Pandas 1.0.0 brings a number of API improvements that make it easier to integrate with existing DRF projects.

### New Functionality
  * Support mixing with DRP renderers with regular DRF renderers, including in `REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"]` (#28)
  * Better detection of default index field name (#13, #29)
  * Include index field(s) in default JSON output (#29).  The `orient` parameter now defaults to a DRP-specific `"records-index"`, which is like `"records"` but calls `reset_index()` before rendering.

### Bug Fixes
  * Don't crash if `"id"` is not a serializer field (#13)
  * Fix null value handling in `PandasScatterSerializer` (2636cc4)

### Documentation Improvements
  * Supported URL parameters for JSON output (#26)
  * `DateTimeField` serialization tips (#27)
  * `django-pandas` integration (#11)
  *  HTML output and integration with [wq/chartapp.js](../@wq/chart.md) (#2)
