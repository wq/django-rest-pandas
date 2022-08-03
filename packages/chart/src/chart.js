import * as d3 from 'd3';

var chart = {};

function _trans(x, y, off) {
    if (off) {
        x -= 0.5;
        y -= 0.5;
    }
    return 'translate(' + x + ',' + y + ')';
}

function _selectOrAppend(sel, name, cls) {
    var selector = name;
    if (cls) {
        selector += '.' + cls;
    }
    var elem = sel.select(selector);
    if (elem.empty()) {
        elem = sel.append(name);
        if (cls) {
            elem.attr('class', cls);
        }
    }
    return elem;
}

// General chart configuration
chart.base = function () {
    var width = 700,
        height = 300,
        padding = 7.5,
        marginGroups = {
            padding: { left: 10, right: 10, top: 10, bottom: 10 },
            xaxis: { bottom: 20 },
        },
        viewBox = true,
        nestedSvg = false,
        renderBackground = false,
        chartover = false,
        chartout = false,
        xscale = null,
        xscalefn = d3.scaleLinear,
        xnice = null,
        xticks = null,
        yscales = {},
        yscalefn = d3.scaleLinear,
        cscale = d3.scaleOrdinal(d3.schemeCategory10),
        outerFill = '#f3f3f3',
        innerFill = '#eee',
        legend = null,
        leftYAxis = true;

    // Accessors for entire data object
    var datasets = function (d) {
        if (d.data) {
            return d.data;
        }
        return d;
    };
    var legendItems = function (d) {
        return datasets(d);
    };

    // Accessors for individual datasets
    var id = function (dataset) {
        return dataset.id;
    };
    var label = function (dataset) {
        return dataset.label;
    };
    var items = function (dataset) {
        return dataset.data || dataset.list;
    };
    var legendItemId = function (d) {
        return id(d);
    };
    var legendItemLabel = function (d) {
        return label(d);
    };

    var xvalue = function (d) {
        /* eslint no-unused-vars: off */
        throw 'xvalue accessor not defined!';
    };
    var yvalue = function (d) {
        /* eslint no-unused-vars: off */
        throw 'yvalue accessor not defined!';
    };
    var xunits = function (dataset) {
        /* eslint no-unused-vars: off */
        return null;
    };
    var xmax = function (dataset) {
        return d3.max(items(dataset), xvalue);
    };
    var xmin = function (dataset) {
        return d3.min(items(dataset), xvalue);
    };
    var xset = function (d) {
        var xvals = new Set();
        datasets(d).forEach(function (dataset) {
            items(dataset).forEach(function (d) {
                xvals.add(xvalue(d));
            });
        });
        return xvals.values().map(function (d) {
            return isNaN(+d) ? d : +d;
        });
    };

    var yunits = function (dataset) {
        return dataset.units;
    };
    var ymax = function (dataset) {
        return d3.max(items(dataset), yvalue);
    };
    var ymin = function (dataset) {
        return d3.min(items(dataset), yvalue);
    };
    // Accessors for individual items
    var xscaled = function (d) {
        return xscale.scale(xvalue(d));
    };
    var yscaled = function (scaleid) {
        var yscale = yscales[scaleid];
        return function (d) {
            return yscale.scale(yvalue(d));
        };
    };
    var itemid = function (d) {
        return xvalue(d) + '=' + yvalue(d);
    };

    // Rendering functions (should be overridden)
    var init = function (datasets, opts) {
        /* eslint no-unused-vars: off */
    };
    var render = function (dataset) {
        /* eslint no-unused-vars: off */
    };
    var wrapup = function (datasets, opts) {
        /* eslint no-unused-vars: off */
    };

    // Legend item rendering
    var legendItemShape = function (sid) {
        /* eslint no-unused-vars: off */
        return 'rect';
    };
    var rectStyle = function (sid) {
        var color = cscale(sid);
        return function (sel) {
            sel.attr('x', -3)
                .attr('y', -3)
                .attr('width', 6)
                .attr('height', 6)
                .attr('fill', color);
        };
    };
    var circleStyle = function (sid) {
        var color = cscale(sid);
        return function (sel) {
            sel.attr('r', 3)
                .attr('fill', color)
                .attr('stroke', 'black')
                .attr('stroke-width', 0.2)
                .attr('cursor', 'pointer');
        };
    };
    var legendItemStyle = function (sid) {
        return rectStyle(sid);
    };

    // Generate translation function xscale + given yscale
    var translate = function (scaleid) {
        var yfn = yscaled(scaleid);
        return function (d) {
            var x = xscaled(d);
            var y = yfn(d);
            return _trans(x, y);
        };
    };

    // Plot using given selection (usually one object, but wrapped as array)
    function plot(sel) {
        if (nestedSvg) {
            sel = _selectOrAppend(sel, 'svg', nestedSvg);
        }
        sel.each(_plot);
    }

    // The actual work
    function _plot(data) {
        if (legend === null || legend.auto) {
            _positionLegend.call(this, legendItems(data));
        }
        _computeScales(datasets(data));
        if (xunits(data)) {
            plot.setMargin('xaxislabel', { bottom: 15 });
        }
        var ordinal = xscalefn().bandwidth || false;
        var svg = d3.select(this);
        var uid =
            svg.attr('data-wq-uid') || Math.round(Math.random() * 1000000);
        svg.attr('data-wq-uid', uid);
        var vbstr;
        if (viewBox) {
            if (viewBox === true) {
                vbstr = '0 0 ' + width + ' ' + height;
            } else {
                vbstr = viewBox;
            }
            svg.attr('viewBox', vbstr);
        }
        var cwidth = width - padding - padding;
        var cheight = height - padding - padding;
        var margins = plot.getMargins();
        var gwidth = cwidth - margins.left - margins.right;
        var gheight = cheight - margins.top - margins.bottom;
        var cbottom = cheight - margins.bottom;
        var opts = {
            padding: padding,
            gwidth: gwidth,
            gheight: gheight,
            cwidth: cwidth,
            cheight: cheight,
        };
        init.call(this, datasets(data), opts);

        // Clip for inner graphing area
        var clipId = 'clip' + uid;
        var defs = _selectOrAppend(svg, 'defs');

        // Webkit can't select clipPath #83438
        var clip = defs.select('#' + clipId);

        if (clip.empty()) {
            clip = defs.append('clipPath').attr('id', clipId);
            clip.append('rect');
        }
        clip.select('rect').attr('width', gwidth).attr('height', gheight);

        // Outer chart area (includes legends, axes & actual graph)
        var outer = _selectOrAppend(svg, 'g', 'outer');
        outer.attr('transform', _trans(padding, padding, true));
        _selectOrAppend(outer, 'rect')
            .attr('width', cwidth)
            .attr('height', cheight)
            .attr('fill', outerFill);

        // Inner graphing area (clipped)
        var inner = _selectOrAppend(outer, 'g', 'inner')
            .attr('clip-path', 'url(#' + clipId + ')')
            .attr('transform', _trans(margins.left, margins.top));
        _selectOrAppend(inner, 'rect')
            .attr('width', gwidth)
            .attr('height', gheight)
            .attr('fill', innerFill);
        if (chartover) {
            inner.on('mouseover', chartover(data));
            inner.on('mousemove', chartover(data));
        }
        if (chartout) {
            inner.on('mouseout', chartout(data));
        }

        // Create actual scale & axis objects
        xscale.scale = xscalefn();
        if (ordinal) {
            xscale.scale
                .domain(xset(data).sort(d3.ascending))
                .range([0, gwidth])
                .padding(0.5);
        } else {
            xscale.scale.domain([xscale.xmin, xscale.xmax]).range([0, gwidth]);
        }
        if (xscale.scale.nice && xnice) {
            xscale.scale.nice(xnice);
        }

        xscale.axis = d3.axisBottom().scale(xscale.scale);
        if (xticks) {
            xscale.axis.ticks(xticks);
        }

        for (var scaleid in yscales) {
            var scale = yscales[scaleid];
            var domain, axisfn;
            if (scale.invert) {
                domain = [scale.ymax, scale.ymin];
            } else {
                domain = [scale.ymin, scale.ymax];
            }
            if (scale.orient == 'right') {
                axisfn = d3.axisRight;
            } else {
                axisfn = d3.axisLeft;
            }
            scale.scale = yscalefn().domain(domain).nice().range([gheight, 0]);

            scale.axis = axisfn().scale(scale.scale);
        }

        // Render each dataset
        if (renderBackground) {
            var background = _selectOrAppend(inner, 'g', 'background')
                .selectAll('g.dataset-background')
                .data(datasets(data), id);
            background
                .enter()
                .append('g')
                .attr('class', 'dataset-background')
                .merge(background)
                .each(renderBackground);
            background.exit().remove();
        }
        var series = _selectOrAppend(inner, 'g', 'datasets')
            .selectAll('g.dataset')
            .data(datasets(data), id);
        series
            .enter()
            .append('g')
            .attr('class', 'dataset')
            .merge(series)
            .each(render);
        series.exit().remove();

        // Render axes
        var xaxis = _selectOrAppend(outer, 'g', 'xaxis')
                .attr('transform', _trans(margins.left, cbottom))
                .call(xscale.axis),
            xlabel = xunits(data);
        if (xlabel) {
            _selectOrAppend(xaxis, 'text', 'axislabel')
                .text(xlabel)
                .attr('text-anchor', 'middle')
                .attr('font-weight', 'bold')
                .attr('fill', '#000')
                .attr('transform', function () {
                    return 'translate(' + gwidth / 2 + ', 30)';
                });
        }

        var yaxes = outer
            .selectAll('g.axis')
            .data(Object.values(yscales), function (s) {
                return s.id;
            });
        var newaxes = yaxes.enter().append('g').attr('class', 'axis');
        newaxes.append('text');
        newaxes
            .merge(yaxes)
            .attr('transform', function (d) {
                var x;
                if (d.orient == 'left') {
                    x = margins.left;
                } else {
                    x = cwidth - margins.right;
                }
                var y = margins.top;
                return _trans(x, y);
            })
            .each(function (d) {
                var axis = d3.select(this);
                axis.call(d.axis);
                axis.select('text')
                    .text(d.id || '')
                    .attr('text-anchor', 'middle')
                    .attr('font-weight', 'bold')
                    .attr('fill', '#000')
                    .attr('transform', function () {
                        if (d.orient == 'left') {
                            return (
                                'rotate(-90),' +
                                'translate(-' +
                                gheight / 2 +
                                ',-30)'
                            );
                        } else {
                            return (
                                'rotate(90),' +
                                'translate(' +
                                gheight / 2 +
                                ',-30)'
                            );
                        }
                    });
            });
        yaxes.exit().remove();

        if (legend && legend.position) {
            _renderLegend.call(this, legendItems(data), opts);
        } else {
            outer.select('g.legend').remove();
        }
        wrapup.call(this, datasets(data), opts);
    }

    function _positionLegend(items) {
        var rows = items.length;
        if (rows > 5) {
            plot.legend({
                position: 'right',
                size: 120,
                auto: true,
            });
        } else {
            plot.legend({
                position: 'bottom',
                size: rows * 19 + 19,
                auto: true,
            });
        }
    }

    // Compute horizontal & vertical scales
    // - may be more than one vertical scale if there are different units
    function _computeScales(datasets) {
        datasets.forEach(function (dataset) {
            if (!xscale) {
                xscale = {
                    xmin: Infinity,
                    xmax: -Infinity,
                    auto: true,
                };
            }
            if (xscale.auto) {
                xscale.xmax = d3.max([xscale.xmax, xmax(dataset)]);
                xscale.xmin = d3.min([xscale.xmin, xmin(dataset)]);
                if (xscale.xmax == xscale.xmin) {
                    xscale.xmax += 1;
                }
            }

            var scaleid = yunits(dataset);
            if (!yscales[scaleid]) {
                yscales[scaleid] = {
                    ymin: 0,
                    ymax: 0,
                    auto: true,
                };
            }
            var yscale = yscales[scaleid];
            if (!yscale.id) {
                yscale.id = scaleid;
            }
            if (!yscale.orient) {
                yscale.orient = leftYAxis ? 'left' : 'right';
                leftYAxis = !leftYAxis;
            }
            if (!yscale.sets) {
                yscale.sets = 0;
            }
            yscale.sets++;
            if (yscale.auto) {
                yscale.ymax = d3.max([yscale.ymax, ymax(dataset)]);
                yscale.ymin = d3.min([yscale.ymin, ymin(dataset)]);
                if (yscale.ymax == yscale.ymin) {
                    yscale.ymax += 1;
                }
            }
        });
        var ymargin = { left: 35 };
        if (Object.keys(yscales).length > 1) {
            ymargin.right = 35;
        }
        plot.setMargin('yaxis', ymargin);
    }

    function _renderLegend(items, opts) {
        var svg = d3.select(this),
            outer = svg.select('g.outer'),
            margins = plot.getMargins({ ignore: 'xaxislabel' }),
            legendX,
            legendY,
            legendW,
            legendH;

        if (legend.position == 'bottom') {
            legendX = margins.left;
            legendY = opts.cheight - margins.bottom + 30;
            legendW = opts.gwidth;
            legendH = legend.size;
        } else {
            legendX = opts.cwidth - legend.size - 10;
            legendY = margins.top;
            legendW = legend.size;
            legendH = opts.gheight;
        }

        var leg = _selectOrAppend(outer, 'g', 'legend').attr(
            'transform',
            _trans(legendX, legendY)
        );
        _selectOrAppend(leg, 'rect')
            .attr('width', legendW)
            .attr('height', legendH)
            .attr('fill', 'white')
            .attr('stroke', '#999');

        var legitems = leg.selectAll('g.legenditem').data(items, legendItemId);
        var newitems = legitems.enter().append('g').attr('class', 'legenditem');
        newitems
            .append('g')
            .attr('class', 'data')
            .each(function (d) {
                var g = d3.select(this),
                    sid = legendItemId(d);
                g.on('click', function (d) {
                    _toggleSeries(d, svg);
                });
                g.append(legendItemShape(sid));
                g.append('text')
                    .attr('font-family', 'sans-serif')
                    .attr('font-size', '13px')
                    .attr('cursor', 'pointer');
            });
        newitems.merge(legitems).each(function (d, i) {
            var g = d3.select(this).select('g.data'),
                sid = legendItemId(d);
            g.attr('transform', _trans(14, 18 + i * 20));
            g.select(legendItemShape(sid)).call(legendItemStyle(sid));
            g.select('text')
                .text(legendItemLabel(d))
                .attr('transform', _trans(10, 5));
        });
        legitems.exit().remove();
    }

    var _hidden = {};

    function _toggleSeries(dataset, svg) {
        var sid = legendItemId(dataset);
        _hidden[sid] = !_hidden[sid];
        _updateHidden(svg);
    }
    function _updateHidden(svg) {
        svg.selectAll('g.dataset-background').style('display', function (d) {
            var sid = legendItemId(d);
            if (_hidden[sid]) {
                return 'none';
            }
        });
        svg.selectAll('g.dataset').style('display', function (d) {
            var sid = legendItemId(d);
            if (_hidden[sid]) {
                return 'none';
            }
        });
        svg.selectAll('g.legenditem').style('opacity', function (d) {
            var sid = legendItemId(d);
            if (_hidden[sid]) {
                return 0.5;
            }
        });
    }

    // Getters/setters for chart configuration
    plot.width = function (val) {
        if (!arguments.length) {
            return width;
        }
        width = val;
        return plot;
    };
    plot.height = function (val) {
        if (!arguments.length) {
            return height;
        }
        height = val;
        return plot;
    };
    plot.viewBox = function (val) {
        if (!arguments.length) {
            return viewBox;
        }
        viewBox = val;
        return plot;
    };
    plot.nestedSvg = function (val) {
        if (!arguments.length) {
            return nestedSvg;
        }
        nestedSvg = val;
        return plot;
    };
    plot.outerFill = function (val) {
        if (!arguments.length) {
            return outerFill;
        }
        outerFill = val;
        return plot;
    };
    plot.innerFill = function (val) {
        if (!arguments.length) {
            return innerFill;
        }
        innerFill = val;
        return plot;
    };
    plot.legend = function (val) {
        if (!arguments.length) {
            return legend;
        }
        legend = val || {};
        var lmargin = {};
        if (legend.position == 'bottom') {
            lmargin.bottom = legend.size + 10;
        } else if (legend.position == 'right') {
            lmargin.right = legend.size + 10;
        }

        plot.setMargin('legend', lmargin);
        return plot;
    };
    plot.xscale = function (val) {
        if (!arguments.length) {
            return xscale;
        }
        xscale = val;
        return plot;
    };
    plot.xscalefn = function (fn) {
        if (!arguments.length) {
            return xscalefn;
        }
        xscalefn = fn;
        return plot;
    };
    plot.xscaled = function (fn) {
        if (!arguments.length) {
            return xscaled;
        }
        xscaled = fn;
        return plot;
    };
    plot.xnice = function (val) {
        if (!arguments.length) {
            return xnice;
        }
        xnice = val;
        return plot;
    };
    plot.xticks = function (val) {
        if (!arguments.length) {
            return xticks;
        }
        xticks = val;
        return plot;
    };
    plot.yscales = function (val) {
        if (!arguments.length) {
            return yscales;
        }
        yscales = val;
        return plot;
    };
    plot.yscalefn = function (fn) {
        if (!arguments.length) {
            return yscalefn;
        }
        yscalefn = fn;
        return plot;
    };
    plot.yscaled = function (fn) {
        if (!arguments.length) {
            return yscaled;
        }
        yscaled = fn;
        return plot;
    };
    plot.cscale = function (fn) {
        if (!arguments.length) {
            return cscale;
        }
        cscale = fn;
        return plot;
    };

    // Getters/setters for accessors
    plot.datasets = function (fn) {
        if (!arguments.length) {
            return datasets;
        }
        datasets = fn;
        return plot;
    };
    plot.id = function (fn) {
        if (!arguments.length) {
            return id;
        }
        id = fn;
        return plot;
    };
    plot.label = function (fn) {
        if (!arguments.length) {
            return label;
        }
        label = fn;
        return plot;
    };
    plot.legendItems = function (fn) {
        if (!arguments.length) {
            return legendItems;
        }
        legendItems = fn;
        return plot;
    };
    plot.legendItemId = function (fn) {
        if (!arguments.length) {
            return legendItemId;
        }
        legendItemId = fn;
        return plot;
    };
    plot.legendItemLabel = function (fn) {
        if (!arguments.length) {
            return legendItemLabel;
        }
        legendItemLabel = fn;
        return plot;
    };
    plot.items = function (fn) {
        if (!arguments.length) {
            return items;
        }
        items = fn;
        return plot;
    };
    plot.yunits = function (fn) {
        if (!arguments.length) {
            return yunits;
        }
        yunits = fn;
        return plot;
    };
    plot.xunits = function (fn) {
        if (!arguments.length) {
            return xunits;
        }
        xunits = fn;
        return plot;
    };
    plot.xvalue = function (fn) {
        if (!arguments.length) {
            return xvalue;
        }
        xvalue = fn;
        return plot;
    };
    plot.xmin = function (fn) {
        if (!arguments.length) {
            return xmin;
        }
        xmin = fn;
        return plot;
    };
    plot.xmax = function (fn) {
        if (!arguments.length) {
            return xmax;
        }
        xmax = fn;
        return plot;
    };
    plot.xset = function (fn) {
        if (!arguments.length) {
            return xset;
        }
        xset = fn;
        return plot;
    };
    plot.yvalue = function (fn) {
        if (!arguments.length) {
            return yvalue;
        }
        yvalue = fn;
        return plot;
    };
    plot.ymin = function (fn) {
        if (!arguments.length) {
            return ymin;
        }
        ymin = fn;
        return plot;
    };
    plot.ymax = function (fn) {
        if (!arguments.length) {
            return ymax;
        }
        ymax = fn;
        return plot;
    };
    plot.itemid = function (fn) {
        if (!arguments.length) {
            return itemid;
        }
        itemid = fn;
        return plot;
    };

    // Getters/setters for render functions
    plot.init = function (fn) {
        if (!arguments.length) {
            return init;
        }
        init = fn;
        return plot;
    };
    plot.chartover = function (fn) {
        if (!arguments.length) {
            return chartover;
        }
        chartover = fn;
        return plot;
    };
    plot.chartout = function (fn) {
        if (!arguments.length) {
            return chartout;
        }
        chartout = fn;
        return plot;
    };
    plot.renderBackground = function (fn) {
        if (!arguments.length) {
            return renderBackground;
        }
        renderBackground = fn;
        return plot;
    };
    plot.render = function (fn) {
        if (!arguments.length) {
            return render;
        }
        render = fn;
        return plot;
    };
    plot.wrapup = function (fn) {
        if (!arguments.length) {
            return wrapup;
        }
        wrapup = fn;
        return plot;
    };
    plot.translate = function (fn) {
        if (!arguments.length) {
            return translate;
        }
        translate = fn;
        return plot;
    };
    plot.legendItemShape = function (fn) {
        if (!arguments.length) {
            return legendItemShape;
        }
        legendItemShape = fn;
        return plot;
    };
    plot.legendItemStyle = function (fn) {
        if (!arguments.length) {
            return legendItemStyle;
        }
        legendItemStyle = fn;
        return plot;
    };
    plot.rectStyle = function (fn) {
        if (!arguments.length) {
            return rectStyle;
        }
        rectStyle = fn;
        return plot;
    };
    plot.circleStyle = function (fn) {
        if (!arguments.length) {
            return circleStyle;
        }
        circleStyle = fn;
        return plot;
    };

    // Inner margin has separate getter and setter as it is composed of a
    // number of individually-set components
    plot.setMargin = function (name, offsets) {
        marginGroups[name] = offsets;
        return plot;
    };

    plot.getMargins = function (opts) {
        var margins = {
            left: 0,
            right: 0,
            top: 0,
            bottom: 0,
        };
        for (var name in marginGroups) {
            if (opts && name == opts.ignore) {
                continue;
            }
            for (var dir in marginGroups[name]) {
                var val = marginGroups[name][dir];
                if (val) {
                    margins[dir] += val;
                }
            }
        }
        return margins;
    };

    return plot;
};

// Scatter plot
chart.scatter = function () {
    var plot = chart.base(),
        pointStyle = plot.circleStyle(),
        pointShape,
        xField = 'x',
        yField = 'y',
        pointCutoff = 50;

    plot.xvalue(function (d) {
        return +d[xField];
    })
        .xunits(function (data) {
            return data.xunits || xField;
        })
        .yvalue(function (d) {
            return +d[yField];
        })
        .yunits(function (dataset) {
            return dataset.yunits || yField;
        })
        .legendItemShape(function (sid) {
            return pointShape(sid);
        })
        .legendItemStyle(function (sid) {
            return pointStyle(sid);
        });

    /* To customize points beyond just the color, override these functions */
    pointShape = function (sid) {
        /* eslint no-unused-vars: off */
        return 'circle';
    };
    // pointStyle function is initialized above

    /* To customize lines beyond just the color, override this function */
    var lineStyle = function (sid) {
        var color = plot.cscale()(sid);
        return function (sel) {
            sel.attr('stroke', color);
        };
    };

    var pointover = function (sid) {
        /* eslint no-unused-vars: off */
        return function (d) {
            d3.select(this).selectAll(pointShape(sid)).attr('fill', '#9999ff');
        };
    };
    var pointout = function (sid) {
        /* eslint no-unused-vars: off */
        return function (d) {
            d3.select(this)
                .selectAll(pointShape(sid))
                .attr('fill', plot.cscale()(sid));
        };
    };
    var pointLabel = function (sid) {
        var x = plot.xvalue(),
            y = plot.yvalue();
        return function (d) {
            return sid + ' at ' + x(d) + ': ' + y(d);
        };
    };
    var drawPointsIf = function (dataset) {
        var items = plot.items()(dataset);
        return items && items.length <= pointCutoff;
    };
    var drawLinesIf = function (dataset) {
        var items = plot.items()(dataset);
        return items && items.length > pointCutoff;
    };

    plot.chartover(function (data) {
        return function (evt) {
            var inner = d3.select(this),
                mouse = d3.pointer(evt),
                xscale = plot.xscale(),
                xvalue = plot.xvalue(),
                translate = plot.translate(),
                x = xscale.scale.invert(mouse[0]),
                bisect = d3.bisector(xvalue),
                hoverData = [];
            plot.datasets()(data).forEach(function (dataset) {
                if (!drawLinesIf(dataset)) {
                    return;
                }
                var sid = plot.id()(dataset),
                    items = plot.items()(dataset),
                    yunits = plot.yunits()(dataset),
                    yscaled = plot.yscaled()(yunits),
                    index = bisect.left(items, x),
                    d1 = items[index > 0 ? index - 1 : 0],
                    d2 = items[index < items.length ? index : index - 1],
                    ptx1 = xscale.scale(xvalue(d1)),
                    pty1 = yscaled(d1),
                    dist1 = Math.sqrt(
                        Math.pow(ptx1 - mouse[0], 2) +
                            Math.pow(pty1 - mouse[1], 2)
                    ),
                    ptx2 = xscale.scale(xvalue(d2)),
                    pty2 = yscaled(d2),
                    dist2 = Math.sqrt(
                        Math.pow(ptx2 - mouse[0], 2) +
                            Math.pow(pty2 - mouse[1], 2)
                    ),
                    threshold = 20;
                if (dist1 < threshold || dist2 < threshold) {
                    hoverData.push({
                        id: sid,
                        units: yunits,
                        data: dist1 < dist2 ? d1 : d2,
                    });
                }
            });
            var hover = inner.selectAll('g.line-hover').data(hoverData);
            hover
                .enter()
                .append('g')
                .attr('class', 'line-hover')
                .merge(hover)
                .each(function (d) {
                    var g = d3.select(this).datum(d.data);
                    _selectOrAppend(g, pointShape(d.id))
                        .call(pointStyle(d.id))
                        .attr('transform', translate(d.units));
                    _selectOrAppend(g, 'title').text(pointLabel(d.id));
                });
            hover.exit().remove();
        };
    });

    // Render lines in background to ensure all points are above them
    plot.renderBackground(function (dataset) {
        var items = plot.items()(dataset),
            yunits = plot.yunits()(dataset),
            sid = plot.id()(dataset),
            xscaled = plot.xscaled(),
            yscaled = plot.yscaled()(yunits),
            g = d3.select(this),
            path = g.select('path.data'),
            line = d3.line().x(xscaled).y(yscaled);
        d3.select(g.node().parentNode.parentNode)
            .selectAll('g.line-hover')
            .remove();
        if (!drawLinesIf(dataset)) {
            path.remove();
            return;
        }
        // Generate path element for new datasets
        if (path.empty()) {
            path = g
                .append('path')
                .attr('class', 'data')
                .attr('fill', 'transparent');
        }
        // Update path for new and existing datasets
        path.datum(items).attr('d', line).call(lineStyle(sid));
    });

    plot.render(function (dataset) {
        var items = plot.items()(dataset),
            yunits = plot.yunits()(dataset),
            sid = plot.id()(dataset),
            translate = plot.translate(),
            g = d3.select(this),
            points,
            newpoints;

        if (!drawPointsIf(dataset)) {
            g.selectAll('g.data').remove();
            return;
        }
        points = g.selectAll('g.data').data(items, plot.itemid());

        // Generate elements for new data
        newpoints = points.enter().append('g').attr('class', 'data');
        newpoints.append('title');
        newpoints.append(pointShape(sid));

        // Update elements for new or existing data
        newpoints
            .merge(points)
            .on('mouseover', pointover(sid))
            .on('mouseout', pointout(sid))
            .attr('transform', translate(yunits))
            .select(pointShape(sid))
            .call(pointStyle(sid));
        newpoints.merge(points).select('title').text(pointLabel(sid));

        points.exit().remove();
    });

    // Getters/setters for chart configuration
    plot.pointShape = function (fn) {
        if (!arguments.length) {
            return pointShape;
        }
        pointShape = fn;
        return plot;
    };

    plot.pointStyle = function (fn) {
        if (!arguments.length) {
            return pointStyle;
        }
        pointStyle = fn;
        return plot;
    };

    plot.lineStyle = function (fn) {
        if (!arguments.length) {
            return lineStyle;
        }
        lineStyle = fn;
        return plot;
    };

    plot.pointover = function (fn) {
        if (!arguments.length) {
            return pointover;
        }
        pointover = fn;
        return plot;
    };

    plot.pointout = function (fn) {
        if (!arguments.length) {
            return pointout;
        }
        pointout = fn;
        return plot;
    };

    plot.pointLabel = function (fn) {
        if (!arguments.length) {
            return pointLabel;
        }
        pointLabel = fn;
        return plot;
    };

    plot.xField = function (val) {
        if (!arguments.length) {
            return xField;
        }
        xField = val;
        return plot;
    };

    plot.yField = function (val) {
        if (!arguments.length) {
            return yField;
        }
        yField = val;
        return plot;
    };

    plot.pointCutoff = function (val) {
        if (!arguments.length) {
            return pointCutoff;
        }
        pointCutoff = val;
        return plot;
    };

    plot.drawPointsIf = function (fn) {
        if (!arguments.length) {
            return drawPointsIf;
        }
        drawPointsIf = fn;
        return plot;
    };

    plot.drawLinesIf = function (fn) {
        if (!arguments.length) {
            return drawLinesIf;
        }
        drawLinesIf = fn;
        return plot;
    };

    return plot;
};

// Time series scatter plot
chart.timeSeries = function () {
    var plot = chart.scatter(),
        format = d3.timeFormat('%Y-%m-%d'),
        parse = d3.timeParse('%Y-%m-%d');

    plot.xField('date')
        .xvalue(function (d) {
            var xField = plot.xField();
            return parse(d[xField]);
        })
        .xscalefn(d3.scaleTime)
        .xnice(d3.timeYear)
        .xunits(function (data) {
            /* eslint no-unused-vars: off */
            return null;
        })
        .yField('value')
        .yunits(function (d) {
            return d.units;
        })
        .pointLabel(function (sid) {
            var x = plot.xvalue(),
                y = plot.yvalue();
            return function (d) {
                return sid + ' on ' + format(x(d)) + ': ' + y(d);
            };
        });

    // Getters/setters for chart configuration
    plot.timeFormat = function (val) {
        if (!arguments.length) {
            return format;
        }
        format = d3.timeFormat(val);
        parse = d3.timeParse(val);
        return plot;
    };

    return plot;
};

// Box & whiskers (precomputed)
chart.boxplot = function () {
    var plot = chart.base(),
        r,
        wr,
        offsets = {},
        prefix = 'value-';

    // Accessors for individual items
    var q1 = function (d) {
        return d[prefix + 'q1'];
    };
    var q3 = function (d) {
        return d[prefix + 'q3'];
    };
    var med = function (d) {
        return d[prefix + 'med'];
    };
    var whishi = function (d) {
        return d[prefix + 'whishi'];
    };
    var whislo = function (d) {
        return d[prefix + 'whislo'];
    };

    plot.xscalefn(d3.scalePoint)
        .itemid(function (d) {
            return plot.xvalue()(d);
        })
        .ymin(function (dataset) {
            var items = plot.items();
            return d3.min(items(dataset), function (d) {
                return whislo(d);
            });
        })
        .ymax(function (dataset) {
            var items = plot.items();
            return d3.max(items(dataset), function (d) {
                return whishi(d);
            });
        })
        .init(function (datasets, opts) {
            var step = plot.xset()(datasets).length; // Number of x axis labels
            var slots = step * (datasets.length + 1); // ~How many boxes to fit
            var space = opts.gwidth / slots; // Space available for each box
            r = d3.min([(space * 0.8) / 2, 20]); // "radius" of box (use 80%)
            wr = r / 2; // "radius" of whiskers
            var width = (datasets.length - 1) * space;
            datasets.forEach(function (dataset, i) {
                offsets[plot.id()(dataset)] = i * space - width / 2;
            });
        })
        .render(function (dataset) {
            var items = plot.items()(dataset),
                yunits = plot.yunits()(dataset),
                sid = plot.id()(dataset),
                yscales = plot.yscales(),
                xscale = plot.xscale(),
                xvalue = plot.xvalue();

            function translate(scaleid) {
                var yscale = yscales[scaleid];
                return function (d) {
                    var x = xscale.scale(xvalue(d));
                    var y = yscale.scale(0);
                    return _trans(x, y);
                };
            }

            var boxes = d3
                .select(this)
                .selectAll('g.data')
                .data(items, plot.itemid());
            boxes
                .enter()
                .append('g')
                .attr('class', 'data')
                .merge(boxes)
                .attr('transform', translate(yunits))
                .each(box(sid, yunits));
            boxes.exit().remove();
        });

    function box(sid, yunits) {
        var yscale = plot.yscales()[yunits];
        var color = plot.cscale()(sid);
        return function (d) {
            var dq1 = q1(d),
                dq3 = q3(d),
                dmed = med(d),
                dwhislo = whislo(d),
                dwhishi = whishi(d);
            if (!d || (!dmed && !dwhislo && !dwhishi)) {
                return;
            }
            function y(val) {
                return yscale.scale(val) - yscale.scale(0);
            }

            var box = _selectOrAppend(d3.select(this), 'g', 'box').attr(
                'transform',
                _trans(offsets[sid], 0)
            );
            _selectOrAppend(box, 'line', 'q1')
                .attr('x1', -r)
                .attr('x2', r)
                .attr('y1', y(dq1))
                .attr('y2', y(dq1))
                .attr('stroke-width', 2)
                .attr('stroke', color);
            _selectOrAppend(box, 'line', 'q3')
                .attr('x1', -r)
                .attr('x2', r)
                .attr('y1', y(dq3))
                .attr('y2', y(dq3))
                .attr('stroke-width', 2)
                .attr('stroke', color);
            _selectOrAppend(box, 'line', 'med')
                .attr('x1', -r)
                .attr('x2', r)
                .attr('y1', y(dmed))
                .attr('y2', y(dmed))
                .attr('stroke-width', 2)
                .attr('stroke', color);
            _selectOrAppend(box, 'line', 'iqr-left')
                .attr('x1', -r)
                .attr('x2', -r)
                .attr('y1', y(dq1))
                .attr('y2', y(dq3))
                .attr('stroke-width', 2)
                .attr('stroke', color);
            _selectOrAppend(box, 'line', 'iqr-right')
                .attr('x1', r)
                .attr('x2', r)
                .attr('y1', y(dq1))
                .attr('y2', y(dq3))
                .attr('stroke-width', 2)
                .attr('stroke', color);
            _selectOrAppend(box, 'line', 'w-top')
                .attr('x1', -wr)
                .attr('x2', wr)
                .attr('y1', y(dwhishi))
                .attr('y2', y(dwhishi))
                .attr('stroke', color);
            _selectOrAppend(box, 'line', 'w-bottom')
                .attr('x1', -wr)
                .attr('x2', wr)
                .attr('y1', y(dwhislo))
                .attr('y2', y(dwhislo))
                .attr('stroke', color);
            _selectOrAppend(box, 'line', 'w-q3')
                .attr('x1', 0)
                .attr('x2', 0)
                .attr('y1', y(dwhishi))
                .attr('y2', y(dq3))
                .attr('stroke', color);
            _selectOrAppend(box, 'line', 'w-q1')
                .attr('x1', 0)
                .attr('x2', 0)
                .attr('y1', y(dwhislo))
                .attr('y2', y(dq1))
                .attr('stroke', color);
        };
    }

    // Getters/setters for accessors
    plot.prefix = function (val) {
        if (!arguments.length) {
            return prefix;
        }
        prefix = val;
        return plot;
    };
    plot.q1 = function (fn) {
        if (!arguments.length) {
            return q1;
        }
        q1 = fn;
        return plot;
    };
    plot.q3 = function (fn) {
        if (!arguments.length) {
            return q3;
        }
        q3 = fn;
        return plot;
    };
    plot.med = function (fn) {
        if (!arguments.length) {
            return med;
        }
        med = fn;
        return plot;
    };
    plot.whishi = function (fn) {
        if (!arguments.length) {
            return whishi;
        }
        whishi = fn;
        return plot;
    };
    plot.whislo = function (fn) {
        if (!arguments.length) {
            return whislo;
        }
        whislo = fn;
        return plot;
    };

    return plot;
};

export default chart;
