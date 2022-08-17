import * as d3 from 'd3';
import chart from './chart';
import * as pandas from '@wq/pandas';
import Mustache from 'mustache';

// Exported module variable
var chartapp = {
    name: 'chartapp',
    config: {
        id_template: null,
        label_template: null,
        point_label_template: null,
        width: 700,
        height: 300,
        point_cutoff: 50,
        timeseries_columns: {
            x: 'date',
            y: 'value',
        },
        time_format: '%Y-%m-%d',
        scatter_columns: {
            x: null,
            y: null,
        },
    },
};

chartapp.init = function (conf) {
    chartapp.config = { ...chartapp.config, conf };
};

var customTypes = {};
chartapp.addType = function (name, method, base) {
    if (!base) {
        base = 'base';
    }
    function makePlot() {
        var plot = chart[base]();
        if (method) {
            method(plot);
        }
        return plot;
    }
    chart[name] = makePlot;
    customTypes[name] = base;
};

// wq/app.js plugin
chartapp.run = function ($page) {
    var $svg = $page.find('svg[data-wq-url]');
    if (!$svg.length) {
        return;
    }
    var type = $svg.data('wq-type'),
        url = $svg.data('wq-url');
    if (!type || !url) {
        return;
    }
    if (!chart[type]) {
        console.warn('Unknown chart type ' + type + '!');
        return;
    }

    pandas.get(url).then(function (data) {
        return chartapp.create(data, type, $svg[0]);
    });
};

chartapp.create = function (data, type, elem) {
    var plot = chart[type](),
        baseType = customTypes[type] || type,
        sel = d3.select(elem),
        conf = function (name, parentName) {
            var attrId = 'data-wq-' + name.replace(/_/g, '-'),
                root = chartapp.config,
                obj = parentName ? root[parentName] : root;
            return sel.attr(attrId) || obj[name];
        },
        id = conf('id_template'),
        label = conf('label_template'),
        pointLabel = conf('point_label_template'),
        timeseriesX = conf('x', 'timeseries_columns'),
        timeFormat = conf('time_format'),
        timeseriesY = conf('y', 'timeseries_columns'),
        scatterX = conf('x', 'scatter_columns'),
        scatterY = conf('y', 'scatter_columns'),
        pointCutoff = conf('point_cutoff'),
        width = conf('width'),
        height = conf('height'),
        keys;

    if ((!id || !label) && data.length) {
        keys = Object.keys(data[0])
            .filter(function (key) {
                return key != 'data';
            })
            .map(function (key) {
                return '{{' + key + '}}';
            })
            .sort();
        if (!id) {
            id = keys.join('-');
        }
        if (!label) {
            label = keys.join(' ');
        }
    }
    if (label.indexOf('[[') > -1 && label.indexOf('{{') == -1) {
        label = '{{=[[ ]]=}}' + label;
    }

    plot.id(function (dataset) {
        return Mustache.render(id, dataset);
    })
        .label(function (dataset) {
            return Mustache.render(label, dataset);
        })
        .width(width)
        .height(height);

    if (baseType == 'scatter' || baseType == 'timeSeries') {
        plot.pointCutoff(pointCutoff);
        if (pointLabel) {
            if (
                pointLabel.indexOf('[[') > -1 &&
                pointLabel.indexOf('{{') == -1
            ) {
                pointLabel = '{{=[[ ]]=}}' + pointLabel;
            }
            plot.pointLabel(function (sid) {
                /* eslint no-unused-vars: off */
                return function (d) {
                    return Mustache.render(pointLabel, d);
                };
            });
        }
    }

    if (baseType == 'boxplot') {
        plot.xvalue(function (d) {
            var prefix = plot.prefix(),
                key = Object.keys(d).filter(function (key) {
                    return key.indexOf(prefix) == -1;
                })[0];
            return d[key];
        });
    } else if (baseType == 'scatter') {
        if ((!scatterX || !scatterY) && data.length) {
            var firstPoint = (data[0].data || [{}])[0] || {};
            keys = Object.keys(firstPoint)
                .filter(function (key) {
                    return key != 'date';
                })
                .sort();
            scatterX = keys[0];
            scatterY = keys[1];
        }
        plot.xField(scatterX);
        plot.yField(scatterY);
    } else if (baseType == 'timeSeries') {
        plot.xField(timeseriesX);
        plot.timeFormat(timeFormat);
        plot.yField(timeseriesY);
    }

    sel.datum(data).call(plot);
};

export default chartapp;
