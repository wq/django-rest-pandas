import React from "react";
import { usePlotly, usePlotData, usePlotLayout } from "../hooks.js";
import PropTypes from "prop-types";

export default function Scatter({ datasets, x, y, label, layout, style }) {
    const Plot = usePlotly(),
        data = usePlotData({
            datasets,
            x,
            y,
            type: "scatter",
            mode: "markers",
            label,
        }),
        _layout = usePlotLayout({ x, y, layout });
    return (
        <Plot
            data={data}
            layout={_layout}
            useResizeHandler
            style={{ flex: 1, ...style }}
        />
    );
}

Scatter.propTypes = {
    datasets: PropTypes.arrayOf(PropTypes.object),
    x: PropTypes.string,
    y: PropTypes.string,
    label: PropTypes.string,
    layout: PropTypes.object,
    style: PropTypes.object,
};
