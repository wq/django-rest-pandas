module.exports = {
    plugins: [["@babel/plugin-transform-react-jsx", { useSpread: true }]],
    env: {
        test: {
            presets: [["@babel/preset-env", { targets: { node: "current" } }]],
        },
        build: {
            plugins: [
                [
                    "transform-rename-import",
                    { original: "^(.+?)\\.jsx$", replacement: "$1.js" },
                ],
            ],
        },
    },
};
