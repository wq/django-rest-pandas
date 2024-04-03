import { modules } from "https://unpkg.com/wq";
import { components } from "https://unpkg.com/@wq/markdown";
import { Analyst } from "https://unpkg.com/@wq/analyst";

const React = modules.react;
const { Paper } = modules["@mui/material"];
const Code = components.code;

export default function CodeDetect(props) {
    const { children: value } = props;
    if (value.includes("// @wq/analyst")) {
        const config = parseConfig(value);
        if (config) {
            return React.createElement(
                Paper,
                { elevation: 3, sx: { p: 1 } },
                React.createElement(Analyst, config),
            );
        } else {
            return React.createElement(Code, {
                children: "// Error parsing @wq/analyst config\n\n" + value,
            });
        }
    } else {
        return React.createElement(Code, props);
    }
}

function parseConfig(value) {
    value = value.replace("// @wq/analyst", "").trim();
    try {
        return JSON.parse(value);
    } catch {
        return null;
    }
}
