import { useState, useEffect, useMemo } from "react";
import { useRouteInfo, useRenderContext } from "@wq/react";
import { get as getPandasCsv } from "@wq/pandas";
import Mustache from "mustache";
import { labelWithIcon } from "./components/Icon.jsx";

export function useAnalyst() {
    const config = useAnalystConfig(),
        [data, dataError] = useAnalystData(
            config.url || null,
            config.data || null,
        ),
        modes = useAnalystModes(data, config),
        [form, options, setOptions] = useAnalystForm(modes);

    return {
        ...config,
        data,
        error: config.error || dataError || (data ? null : "Loading..."),
        modes,
        form,
        options,
        setOptions,
    };
}

export function useAnalystConfig() {
    const {
            page_config: { name, analyst = {} },
        } = useRouteInfo(),
        context = useRenderContext();

    if (!analyst.url) {
        return {
            error: `The config for "${name}" should include an analyst.url property.`,
        };
    }

    return {
        ...analyst,
        url: render(analyst.url, context),
        title: render(analyst.title, context),
    };
}

function render(value, context) {
    if (value) {
        return Mustache.render(value, context);
    } else {
        return value;
    }
}

export function useAnalystData(url, initialData) {
    const [data, setData] = useState(initialData),
        [error, setError] = useState(null);

    useEffect(() => {
        if (!url) {
            return;
        }
        async function loadData() {
            try {
                const data = await getPandasCsv(url, { flatten: true });
                if (data && data.length > 0) {
                    setData(data);
                } else {
                    setError("No data found.");
                }
            } catch (e) {
                console.error(e);
                setError("Error loading data.");
            }
        }
        loadData();
    }, [url]);

    useEffect(() => {
        setData(initialData);
    }, [initialData]);

    return [data, error];
}

export function useAnalystModes(data, config) {
    return useMemo(() => {
        const modes = [],
            columnTypes = findColumns(data);

        if (columnTypes.date || columnTypes.numeric || columnTypes.string) {
            modes.push({ name: "table", label: "Table" });
        }
        if (columnTypes.date && columnTypes.numeric) {
            modes.push({
                name: "series",
                label: "Series",
                dateColumns: columnTypes.date,
                valueColumns: columnTypes.numeric,
            });
        }
        if (columnTypes.numeric && columnTypes.numeric.length > 1) {
            modes.push({
                name: "scatter",
                label: "Scatter",
                dateColumns: columnTypes.date,
                valueColumns: columnTypes.numeric,
            });
        }
        if (columnTypes.numeric) {
            modes.push({
                name: "boxplot",
                label: "Box",
                dateColumns: columnTypes.date,
                valueColumns: columnTypes.numeric,
            });
        }
        if (config && config.modes) {
            return config.modes
                .map((modeName) => modes.find((mode) => mode.name === modeName))
                .filter(Boolean);
        } else {
            return modes;
        }
    }, [data, config]);
}

function findColumns(data) {
    const columns = {},
        datasets = (data && data.datasets) || [{ data: data || [] }];
    for (const dataset of datasets) {
        for (const row of dataset.data) {
            for (const [key, val] of Object.entries(row)) {
                if (isNumeric(val)) {
                    columns[key] = "numeric";
                } else if (isDate(val) && columns[key] !== "numeric") {
                    columns[key] = "date";
                } else if (val && !columns[key]) {
                    columns[key] = "string";
                }
            }
        }
    }
    const columnTypes = {};
    for (const [key, type] of Object.entries(columns)) {
        if (!columnTypes[type]) {
            columnTypes[type] = [];
        }
        columnTypes[type].push(key);
    }
    return columnTypes;
}

function isNumeric(value) {
    return typeof value === "number";
}

function isDate(value) {
    return (
        value instanceof Date ||
        (typeof value === "string" && value.match(/^\d{4}-\d{2}-\d{2}$/))
    );
}

function useAnalystForm(modes) {
    const [options, setOptions] = useState(defaultOptions),
        form = useMemo(
            () => makeForm(modes, options.mode),
            [modes, options.mode],
        );

    useEffect(() => {
        const nextOptions = {},
            currOptions = options || {};
        for (const field of form) {
            if (
                field.choices &&
                field.choices.length > 0 &&
                !currOptions[field.name]
            ) {
                nextOptions[field.name] =
                    field.choices[
                        field.name === "value2" && field.choices.length > 1
                            ? 1
                            : 0
                    ].name;
            } else if (currOptions[field.name] === undefined) {
                nextOptions[field.name] = "";
            }
        }
        if (Object.keys(nextOptions).length > 0) {
            setOptions({ ...options, ...nextOptions });
        }
    }, [form, options]);
    return [form, options, setOptions];
}

const defaultOptions = { mode: "", date: "", value: "", value2: "", group: "" };

function makeForm(modes, currentMode) {
    if (!modes) {
        return null;
    }
    const modeInfo = modes.find((mode) => mode.name === currentMode),
        form = [
            {
                type: modes.length > 1 ? "select one" : "hidden",
                name: "mode",
                label: "",
                bind: { required: true },
                fullwidth: true,
                choices: modes.map(({ name, label }) => ({
                    name,
                    label: labelWithIcon(label, name),
                })),
            },
        ];

    if (modeInfo && modeInfo.dateColumns && modeInfo.dateColumns.length > 0) {
        form.push({
            name: "date",
            type: modeInfo.dateColumns.length > 1 ? "select one" : "hidden",
            label: "Date",
            control:
                modeInfo.dateColumns.length > 1
                    ? { appearance: "select" }
                    : null,
            bind: { required: true },
            choices: modeInfo.dateColumns.map((name) => ({
                name,
                label: name,
            })),
        });
    }

    if (modeInfo && modeInfo.valueColumns && modeInfo.valueColumns.length > 0) {
        form.push({
            name: "value",
            type: modeInfo.valueColumns.length > 1 ? "select one" : "hidden",
            control:
                modeInfo.valueColumns.length > 1
                    ? { appearance: "select" }
                    : null,
            label: currentMode === "scatter" ? "X" : "Value",
            bind: { required: true },
            choices: modeInfo.valueColumns.map((name) => ({
                name,
                label: name,
            })),
        });
        if (currentMode == "scatter") {
            form.push({
                name: "value2",
                type: "select one",
                control: { appearance: "select" },
                label: "Y",
                bind: { required: true },
                choices: modeInfo.valueColumns.map((name) => ({
                    name,
                    label: name,
                })),
            });
        }
    }

    if (currentMode === "boxplot" && modeInfo && modeInfo.dateColumns) {
        form.push({
            name: "group",
            type: "select one",
            control: { appearance: "select" },
            label: "Group",
            bind: { required: true },

            choices: [
                { name: "all", label: "All Data" },
                { name: "year", label: "Year" },
                { name: "month", label: "Month" },
            ],
        });
    }

    return form;
}
