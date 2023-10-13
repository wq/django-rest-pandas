import React from "react";
import { usePlotly, usePlotData, usePlotLayout } from "../hooks.js";
import PropTypes from "prop-types";

export default function Boxplot({ datasets, x, y, group, layout, style }) {
    const Plot = usePlotly(),
        data = usePlotData({ datasets, x, y, type: "box", group, label: x }),
        _layout = usePlotLayout({ x, y, type: "box", layout });
    return (
        <Plot
            data={data}
            layout={_layout}
            useResizeHandler
            style={{ flex: 1, ...style }}
        />
    );
}

Boxplot.propTypes = {
    datasets: PropTypes.arrayOf(PropTypes.object),
    x: PropTypes.string,
    y: PropTypes.string,
    group: PropTypes.string,
    layout: PropTypes.object,
    style: PropTypes.object,
};
