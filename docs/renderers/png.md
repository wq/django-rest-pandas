---
order: 7
tag: image/png
---

# PNG

Django REST Pandas' PNG [renderer class][renderers] provides `image/png` support by calling `plot()` on the DataFrame instance.

This renderer is currently not very customizable, but a simple way to view the data as an image.  Eventually this renderer (and the [SVG renderer][svg]) could become a fallback for clients that can't handle d3.js.

[renderers]: ./index.md
[svg]: ./svg.md
