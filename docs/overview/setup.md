---
order: -2
icon: pin
---

# Getting Started

```bash
# Recommended: create virtual environment
# python3 -m venv venv
# . venv/bin/activate
pip install rest-pandas
```

**NOTE:** Django REST Pandas relies on pandas, which itself relies on NumPy and other scientific Python libraries written in C.  This is usually fine, since pip can use Python Wheels to install precompiled versions.  If you are having trouble installing DRP due to dependency issues, you may need to pre-install pandas using apt or conda.
