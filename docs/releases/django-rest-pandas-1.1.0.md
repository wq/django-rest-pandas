---
repo: django-rest-pandas
date: 2019-03-28
tag: latest
tag_color: primary
---

# DRP 1.1.0

**Django REST Pandas 1.1.0** includes a new filename option (#31), confirmed support for Django 2, and a couple of minor fixes.

### New Functionality
Added a `get_pandas_filename()` view method, for cases where you have users downloading files through the API (#31).  For example:

```python
class TimeSeriesView(PandasView):
    # If a filename is returned, rest_pandas will include the following header:
    # 'Content-Disposition: attachment; filename="Data Export.xlsx"'
    def get_pandas_filename(self, request, format):
        if format in ('xls', 'xlsx'):
            # Use custom filename and Content-Disposition header
            return "Data Export"  # Extension will be appended automatically
        else:
            # Default filename from URL (no Content-Disposition header)
            return None
```

### Bug Fixes
 * Don't crash if `renderer_context` is missing (#34)
 * `PandasBoxplotSerializer`: handle non-numeric columns and duplicate rows (abeb57680f4138f8ac5f92591cc83c5c414bff85)

### Documentation Improvements
 * Test Django 2 support (#35), add wheel and LICENSE for PyPI (#33)
 * Using `rest_pandas` with an existing view (#32, #36)
