import { useState, useEffect, useMemo } from "react";
import config from "./config.js";
import createPlotlyComponent from "react-plotly.js/factory";

const plotlyRef = {},
    defaultLayout = { autosize: true };

export function usePlotly() {
    const [Plot, setPlot] = useState(() => plotlyRef.current);

    useEffect(() => {
        if (plotlyRef.current) {
            return;
        }
        loadPlotly();
        async function loadPlotly() {
            try {
                await import(config.plotly);
                const Plot = createPlotlyComponent(window.Plotly);
                plotlyRef.current = Plot;
                setPlot(() => Plot);
            } catch {
                setPlot(() => ErrorPlot);
            }
        }
    });

    return Plot || LoadingPlot;
}

function LoadingPlot() {
    return "Loading...";
}

function ErrorPlot() {
    return "Error loading Plotly.";
}

export function usePlotLayout({ type, x, y, layout }) {
    return useMemo(
        () => ({
            ...defaultLayout,
            boxmode: type === "box" ? "group" : null,
            ...layout,
            xaxis: { title: x, ...(layout || {}).xaxis },
            yaxis: { title: y, ...(layout || {}).yaxis },
        }),
        [type, x, y, layout],
    );
}

export function usePlotData({ type, mode, datasets, x, y, label, group }) {
    return useMemo(() => {
        const data = (datasets || []).map((dataset) => {
            const trace = {
                type,
                mode,
                name: getLabel(dataset),
                x: [],
                y: [],
                text: [],
            };
            for (const row of dataset.data.slice().sort(valueSort(x))) {
                const [xVal, xNote] = getX(row, x, type, group),
                    [yVal, yNote] = getY(row, y),
                    labelVal = row[label];
                if (xVal !== undefined && yVal !== undefined) {
                    trace.x.push(xVal);
                    trace.y.push(yVal);
                    trace.text.push(
                        [labelVal, xNote, yNote].filter(Boolean).join("<br>") ||
                            null,
                    );
                }
            }
            if (type === "box") {
                trace.boxpoints = "outliers";
            }
            return trace;
        });
        return data;
    }, [datasets, x, y, type, mode, group, label]);
}

function getX(row, x, type, group) {
    const [xVal, xNote] = getVal(row, x);
    if (type === "box") {
        if (group === "year") {
            return [xVal.split("-")[0], xNote];
        } else if (group === "month") {
            return [xVal.split("-").slice(0, 2).join("-"), xNote];
        } else {
            return ["", xNote];
        }
    } else {
        return [xVal, xNote];
    }
}

function getY(row, y) {
    return getVal(row, y);
}

function getVal(row, key) {
    const val = row[key];
    if (
        typeof val === "string" &&
        (val[0] === ">" || val[0] === "<") &&
        !isNaN(+val.slice(1))
    ) {
        return [+val.slice(1), `Note: ${key} ${val}`];
    } else {
        return [val, null];
    }
}

function getLabel(dataset) {
    const label = [];
    for (const [key, val] of Object.entries(dataset)) {
        if (key === "data") {
            continue;
        }
        label.push(val);
    }
    return label.join(" ");
}

function valueSort(field) {
    return (row1, row2) => {
        const value1 = row1[field],
            value2 = row2[field];
        if (value1 > value2) {
            return 1;
        } else if (value1 < value2) {
            return -1;
        } else {
            return 0;
        }
    };
}
