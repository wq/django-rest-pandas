import React from "react";
import { useComponents } from "@wq/react";
import { Series, Scatter, Boxplot } from "@wq/chart";
import { useAnalyst } from "../hooks.js";

export default function Analyst() {
    const { View, Typography, AnalystDownload, AnalystTable, AnalystForm } =
            useComponents(),
        {
            url,
            data,
            error,
            title,
            formats,
            initial_rows,
            initial_order,
            id_column,
            id_url_prefix,
            form,
            options,
            setOptions,
        } = useAnalyst();

    if (error) {
        return (
            <View sx={{ p: 2 }}>
                <Typography>{error}</Typography>
            </View>
        );
    }

    return (
        <View
            style={{
                flex: 1,
                display: "flex",
                flexDirection: "column",
                overflow: "hidden",
            }}
        >
            {formats && (
                <AnalystDownload url={url} title={title} formats={formats} />
            )}
            {!formats && title && <Typography variant="h5">{title}</Typography>}
            {form && (
                <AnalystForm
                    form={form}
                    options={options}
                    setOptions={setOptions}
                />
            )}
            {options.mode === "series" && (
                <Series
                    datasets={data && data.datasets}
                    x={options.date}
                    y={options.value}
                />
            )}
            {options.mode === "scatter" && (
                <Scatter
                    datasets={data && data.datasets}
                    x={options.value}
                    y={options.value2}
                    label={options.date}
                />
            )}
            {options.mode === "boxplot" && (
                <Boxplot
                    datasets={data && data.datasets}
                    x={options.date}
                    y={options.value}
                    group={options.group}
                />
            )}
            {!options.mode ||
                (options.mode === "table" && (
                    <AnalystTable
                        data={data}
                        initial_rows={initial_rows}
                        initial_order={initial_order}
                        id_column={id_column}
                        id_url_prefix={id_url_prefix}
                    />
                ))}
        </View>
    );
}
