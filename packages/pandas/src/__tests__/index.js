import * as pandas from "../index.js";
import mockFetch from "jest-fetch-mock";
import fs from "fs";

beforeAll(() => {
    global.fetch = mockFetch;
});

test("pandas.parse()", () => {
    expect(
        pandas.parse(
            ",val1,val2\n" +
                "site,SITE1,SITE1\n" +
                "parameter,PARAM1,PARAM1\n" +
                "date,,\n" +
                "2014-01-01,0.6,0.3\n" +
                "2014-01-02,0.9,\n",
        ),
    ).toEqual([
        {
            site: "SITE1",
            parameter: "PARAM1",
            data: [
                { date: "2014-01-01", val1: 0.6, val2: 0.3 },
                { date: "2014-01-02", val1: 0.9 },
            ],
        },
    ]);
});

test("pandas.parse() with plain csv", () => {
    expect(
        pandas.parse(
            "date,val1,val2\n" + "2014-01-01,0.6,0.3\n" + "2014-01-02,0.9,\n",
        ),
    ).toEqual([
        {
            data: [
                { date: "2014-01-01", val1: 0.6, val2: 0.3 },
                { date: "2014-01-02", val1: 0.9, val2: "" },
            ],
        },
    ]);
});

test("pandas.get()", async () => {
    mockFetch.mockResponse(fs.readFileSync(__dirname + "/data.csv"));
    var data = await pandas.get("data.csv");
    expect(data).toEqual([
        {
            site: "SITE1",
            parameter: "PARAM1",
            data: [
                { date: "2014-01-01", value: 0.5 },
                { date: "2014-01-02", value: 0.1 },
            ],
        },
        {
            site: "SITE2",
            parameter: "PARAM1",
            data: [
                { date: "2014-01-01", value: 0.5 },
                { date: "2014-01-02", value: 0.5 },
            ],
        },
        {
            site: "SITE3",
            parameter: "PARAM2",
            data: [
                { date: "2014-01-01", value: 0.2 },
                { date: "2014-01-02", value: 0.2 },
            ],
        },
    ]);
});

test("pandas.get() with flatten: true", async () => {
    mockFetch.mockResponse(fs.readFileSync(__dirname + "/data.csv"));
    var data = await pandas.get("data.csv", { flatten: true });
    delete data.datasets;
    expect(data).toEqual([
        {
            site: "SITE1",
            parameter: "PARAM1",
            date: "2014-01-01",
            value: 0.5,
        },
        {
            site: "SITE1",
            parameter: "PARAM1",
            date: "2014-01-02",
            value: 0.1,
        },
        {
            site: "SITE2",
            parameter: "PARAM1",
            date: "2014-01-01",
            value: 0.5,
        },
        {
            site: "SITE2",
            parameter: "PARAM1",
            date: "2014-01-02",
            value: 0.5,
        },
        {
            site: "SITE3",
            parameter: "PARAM2",
            date: "2014-01-01",
            value: 0.2,
        },
        {
            site: "SITE3",
            parameter: "PARAM2",
            date: "2014-01-02",
            value: 0.2,
        },
    ]);
});
