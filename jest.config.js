module.exports = {
    testMatch: ['**/__tests__/**/*.js?(x)'],
    transformIgnorePatterns: [
        '/node_modules/(?!@wq|d3|internmap|delaunator|robust-predicates)',
    ],
};
