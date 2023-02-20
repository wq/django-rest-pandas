import pkg from "./package.json" assert { type: "json" };
import wq from "@wq/rollup-plugin";
import babel from "@rollup/plugin-babel";
import resolve from "@rollup/plugin-node-resolve";
import commonjs from "@rollup/plugin-commonjs";
import replace from "@rollup/plugin-replace";
import terser from "@rollup/plugin-terser";

const banner = `/*
 * ${pkg.name} ${pkg.version}
 * ${pkg.description}
 * (c) 2022-2023, S. Andrew Sheppard
 * https://wq.io/license
 */
`;

const dir = `packages/${pkg.name.replace("@wq/", "")}`;

const config = {
        input: `${dir}/src/index.js`,
        plugins: [
            wq(),
            babel({
                plugins: [
                    "@babel/transform-react-jsx",
                    [
                        "babel-plugin-direct-import",
                        { modules: ["@mui/material", "@mui/icons-material"] },
                    ],
                ],
                babelHelpers: "inline",
            }),
            commonjs(),
            resolve(),
            terser({ keep_fnames: /^([A-Z]|use[A-Z])/ }), // Preserve component & hook names
        ],
        output: {
            file: `${dir}/index.js`,
            banner,
            format: "esm",
            sourcemap: true,
        },
    },
    replaceConfig = {
        "process.env.NODE_ENV": '"production"',
        delimiters: ["", ""],
        preventAssignment: true,
    };

export default [
    // @wq/app plugin (npm main)
    {
        ...config,
        external: [
            "react",
            "prop-types",
            "@wq/react",
            "@wq/pandas",
            "@mui/material",
            "@mui/icons-material",
        ],
        plugins: [
            babel({
                plugins: ["@babel/transform-react-jsx"],
                babelHelpers: "inline",
            }),
        ],
    },
    // wq.app staticfiles plugin (for rest-pandas python package)
    {
        ...config,
        plugins: [replace(replaceConfig), ...config.plugins],
        output: {
            ...config.output,
            file: "rest_pandas/static/app/js/analyst.js",
            sourcemapPathTransform(path) {
                return path.replace("../../../../", "django-rest-pandas/");
            },
        },
    },
];
