import config from "./config.js";

const chart = {
    name: "chart",
    config,
    init(config) {
        Object.assign(this.config, config);
    },
};

export default chart;
export * from "./charts/index.js";
export * from "./hooks.js";
