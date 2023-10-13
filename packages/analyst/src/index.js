import * as components from "./components/index.js";
import * as views from "./views/index.js";
import * as icons from "./icons.js";
import chart from "@wq/chart";
import version from "./version.js";

const analyst = {
    name: "analyst",
    dependencies: [chart],
    version,
    components: { ...components },
    views: { ...views },
    icons: { ...icons },
};

export default analyst;

export * from "./components/index.js";
export * from "./views/index.js";
export * from "./hooks.js";
