/**
 * @jest-environment jsdom
 */

import chartapp from "../index.js";
import mockFetch from "jest-fetch-mock";
import fs from "fs";

beforeAll(() => {
    global.fetch = mockFetch;
});

test("timeSeries chart", async () => {
    mockFetch.mockResponse(fs.readFileSync(__dirname + "/data.csv"));
    document.body.innerHTML = `<svg
        data-wq-url="data.csv"
        data-wq-type="timeSeries"
        data-wq-id-template="{site}-{parameter}"
        ></svg>
    `;
    var svg = document.body.firstChild;
    var $mockPage = {
        find: () => $mockPage,
        data: (key) => {
            return svg.dataset[key.replace(/-(.)/g, (a) => a[1].toUpperCase())];
        },
        length: 1,
        0: svg,
    };
    await chartapp.run($mockPage, {});
    await new Promise((res) => setTimeout(res, 1000));

    const byClass = (name) => svg.getElementsByClassName(name);
    expect(byClass("dataset")).toHaveLength(3);
    expect(byClass("axis")).toHaveLength(1);
    expect(byClass("data")).toHaveLength(9);
});
