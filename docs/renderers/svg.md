---
order: 8
tag: image/svg
---

# SVG

Django REST Pandas' SVG [renderer class][renderers] provides `image/svg` support by calling `plot()` on the DataFrame instance.

This renderer is currently not very customizable, but a simple way to view the data as an image.  Eventually this renderer (and the [PNG renderer][png]) could become a fallback for clients that can't handle d3.js.

[renderers]: ./index.md
[png]: ./png.md
