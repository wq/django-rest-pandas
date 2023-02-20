import * as components from "./components/index";
import * as views from "./views/index";
import * as icons from "./icons";
import version from "./version";

const analyst = {
    name: "analyst",
    version,
    components: { ...components },
    views: { ...views },
    icons: { ...icons },
};

export default analyst;

export * from "./components/index";
export * from "./views/index";
