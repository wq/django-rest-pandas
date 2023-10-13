import React, { useEffect, useState, useMemo, useCallback } from "react";
import { Badge, Menu, MenuItem } from "@mui/material";
import { useAnalystData } from "../hooks.js";
import { useComponents, useNav, useApp } from "@wq/react";
import PropTypes from "prop-types";

export default function AnalystTable({
    data: initialData,
    url,
    initial_rows,
    initial_order,
    id_column,
    id_url_prefix,
    compact,
}) {
    const [data, error] = useAnalystData(url, initialData),
        [columns, setColumns] = useState(),
        [filters, setFilters] = useState({}),
        [orders, setOrders] = useState(initial_order || {}),
        pagination = initial_rows !== "all",
        [rowsPerPage, setRowsPerPage] = useState(
            pagination ? initial_rows || 50 : null,
        ),
        [page, setPage] = useState(0),
        {
            Typography,
            Table,
            TableHead,
            TableBody,
            TableRow,
            TableTitle,
            TableCell,
            TableContainer,
            TablePagination,
            IconButton,
        } = useComponents(),
        app = useApp(),
        appNav = useNav(),
        prefixIsAppUrl =
            id_url_prefix &&
            new URL(id_url_prefix, window.location.origin)
                .toString()
                .startsWith(
                    new URL(app.base_url, window.location.origin).toString(),
                ),
        nav = (id) => {
            const url = `${id_url_prefix}${id}`;
            if (prefixIsAppUrl) {
                appNav(url);
            } else {
                window.location.href = url;
            }
        };

    useEffect(() => {
        if (!data || data.length === 0) {
            return;
        }
        let keys = Object.keys(data[0]),
            allKeys = new Set(keys);
        for (const row of data) {
            const rowKeys = Object.keys(row);
            if (rowKeys.length > keys.length) {
                keys = rowKeys;
            }
            for (const key of rowKeys) {
                if (!allKeys.has(key)) {
                    allKeys.add(key);
                }
            }
        }

        for (const key of allKeys) {
            if (!keys.includes(key)) {
                keys.push(key);
            }
        }

        const nextColumns = keys.map((key) => {
            const metaKeys = {},
                colFilters = { ...filters };
            delete colFilters[key];
            data.datasets.forEach((dataset) => {
                if (!matchFilters(dataset, colFilters)) {
                    return;
                }
                Object.entries(dataset).forEach(([key, value]) => {
                    if (key === "data") {
                        return;
                    }
                    if (!metaKeys[key]) {
                        metaKeys[key] = {};
                    }
                    metaKeys[key][value] =
                        (metaKeys[key][value] || 0) + dataset.data.length;
                });
            });

            const colInfo = { name: key };
            if (metaKeys[key]) {
                colInfo.values = Object.entries(metaKeys[key])
                    .sort((kval1, kval2) => sort(kval1[0], kval2[0]))
                    .map(([key, value]) => ({
                        value: key,
                        count: value,
                    }));
            }
            return colInfo;
        });

        setColumns(nextColumns);
    }, [data, filters]);

    const sortedData = useMemo(() => {
        if (!data) {
            return null;
        }
        if (
            Object.keys(orders).length === 0 &&
            Object.keys(filters).length === 0
        ) {
            return data;
        }
        return data
            .filter((row) => matchFilters(row, filters))
            .sort((row1, row2) => {
                let result = 0;
                Object.entries(orders).forEach(([key, keyOrder]) => {
                    if (result) {
                        return;
                    }
                    result = sort(row1[key], row2[key], keyOrder);
                });
                return result;
            });
    }, [data, filters, orders]);

    const slicedData = useMemo(() => {
        if (!sortedData) {
            return null;
        }
        if (!pagination) {
            return sortedData;
        }
        return sortedData.slice(
            page * rowsPerPage,
            page * rowsPerPage + rowsPerPage,
        );
    }, [sortedData, pagination, page, rowsPerPage]);

    const toggleOrder = (name) => {
        let nextOrders = { ...orders };
        if (!orders[name]) {
            nextOrders = {
                [name]: "asc",
                ...nextOrders,
            };
        } else if (orders[name] === "asc") {
            nextOrders[name] = "desc";
        } else {
            delete nextOrders[name];
        }

        setOrders(nextOrders);
    };

    const toggleFilter = (name, value) => {
        const nextFilters = { ...filters };
        if (!filters[name]) {
            nextFilters[name] = new Set([value]);
        } else if (!nextFilters[name].has(value)) {
            nextFilters[name].add(value);
        } else {
            nextFilters[name].delete(value);
            if (nextFilters[name].size === 0) {
                delete nextFilters[name];
            }
        }
        setFilters(nextFilters);
    };

    const resetFilter = (name) => {
        const nextFilters = { ...filters };
        delete nextFilters[name];
        setFilters(nextFilters);
    };

    const FullHeader = useCallback(
        (column) => {
            if (column.name == id_column) {
                return <TableTitle />;
            }

            return (
                <TableTitle key={column.name}>
                    <div
                        style={{
                            display: "flex",
                            alignItems: "center",
                            marginLeft: -8,
                            borderLeft: "2px solid #ccc",
                            paddingLeft: 8,
                            marginRight: -16,
                        }}
                    >
                        <span
                            style={{
                                flex: 1,
                                fontWeight: "bold",
                            }}
                        >
                            {column.name}
                        </span>
                        <Badge
                            overlap="circular"
                            badgeContent={
                                Object.keys(orders).indexOf(column.name) + 1
                            }
                        >
                            <IconButton
                                size="small"
                                icon={
                                    orders[column.name] === "desc"
                                        ? "sort-desc"
                                        : orders[column.name]
                                        ? "sort-asc"
                                        : "sort-none"
                                }
                                color={orders[column.name] && "secondary"}
                                onClick={() => toggleOrder(column.name)}
                            />
                        </Badge>
                        {column.values && (
                            <ColumnFilter
                                {...column}
                                filter={filters[column.name]}
                                toggleFilter={(value) =>
                                    toggleFilter(column.name, value)
                                }
                                resetFilter={() => resetFilter(column.name)}
                            />
                        )}
                    </div>
                </TableTitle>
            );
        },
        [orders, toggleOrder, filters, toggleFilter, resetFilter],
    );

    const CompactHeader = useCallback(
        (column) => {
            if (column.name === id_column) {
                return null;
            } else if (column.values) {
                return (
                    <TableTitle style={{ cursor: "pointer" }}>
                        <ColumnFilter
                            {...column}
                            textButton
                            filter={filters[column.name]}
                            toggleFilter={(value) =>
                                toggleFilter(column.name, value)
                            }
                            resetFilter={() => resetFilter(column.name)}
                        />
                    </TableTitle>
                );
            } else {
                return (
                    <TableTitle
                        style={{ cursor: "pointer" }}
                        onClick={() => toggleOrder(column.name)}
                    >
                        <span style={{ fontWeight: "bold" }}>
                            {column.name}
                        </span>
                        {orders[column.name] === "desc"
                            ? " ↓"
                            : orders[column.name]
                            ? " ↑"
                            : ""}
                    </TableTitle>
                );
            }
        },
        [filters, toggleFilter, resetFilter, orders, toggleOrder],
    );

    const ColumnHeader = compact ? CompactHeader : FullHeader,
        Cell = useCallback(
            (cell) => {
                if (cell.column.name === id_column) {
                    if (compact) {
                        return null;
                    } else {
                        return (
                            <TableCell>
                                <CellLink {...cell} nav={nav} />
                            </TableCell>
                        );
                    }
                } else if (compact && id_column) {
                    const id = cell.row[id_column];
                    return (
                        <TableCell
                            style={{ cursor: "pointer" }}
                            onClick={() => nav(id)}
                        >
                            <CellValue {...cell} />
                        </TableCell>
                    );
                } else {
                    return (
                        <TableCell>
                            <CellValue {...cell} />
                        </TableCell>
                    );
                }
            },
            [compact, id_column],
        );

    if (error) {
        return <Typography>{error}</Typography>;
    }
    if (!data) {
        return <Typography>Loading...</Typography>;
    }
    if (!columns) {
        return <Typography>No data.</Typography>;
    }
    if (!sortedData.length) {
        return <Typography>No data matching the current filter(s).</Typography>;
    }

    return (
        <>
            <TableContainer>
                <Table stickyHeader>
                    <TableHead>
                        <TableRow>
                            {columns.map((column) => (
                                <ColumnHeader key={column.name} {...column} />
                            ))}
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {slicedData.map((row, i) => (
                            <TableRow key={id_column ? row[id_column] : i}>
                                {columns.map((column) => (
                                    <Cell
                                        key={column.name}
                                        column={column}
                                        row={row}
                                    />
                                ))}
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </TableContainer>
            {pagination && (
                <TablePagination
                    component="div"
                    style={{ minHeight: 52 }}
                    count={sortedData.length}
                    page={page}
                    rowsPerPage={rowsPerPage}
                    onPageChange={(evt, page) => setPage(page)}
                    onRowsPerPageChange={(evt) =>
                        setRowsPerPage(evt.target.value)
                    }
                />
            )}
        </>
    );
}

AnalystTable.propTypes = {
    data: PropTypes.arrayOf(PropTypes.object),
    url: PropTypes.string,
    initial_rows: PropTypes.oneOfType([PropTypes.number, PropTypes.string]),
    compact: PropTypes.bool,
    initial_order: PropTypes.object,
    id_column: PropTypes.string,
    id_url_prefix: PropTypes.string,
};

function ColumnFilter({
    name,
    values,
    filter,
    toggleFilter,
    resetFilter,
    textButton,
}) {
    const [anchorEl, setAnchorEl] = useState(null),
        { IconButton, CheckboxButton } = useComponents(),
        menuId = `${name}-menu`;
    const Component = textButton ? TextButton : IconButton;
    return (
        <>
            <Component
                aria-controls={menuId}
                onClick={(evt) => setAnchorEl(evt.target)}
                size="small"
                icon="filter"
                color={filter && "secondary"}
                title={name}
            />
            <Menu
                id={menuId}
                anchorEl={anchorEl}
                open={!!anchorEl}
                onClose={() => setAnchorEl(null)}
            >
                <MenuItem onClick={resetFilter}>
                    <CheckboxButton checked={!filter} /> All {name}s
                </MenuItem>
                {values.map(({ value, count }) => (
                    <MenuItem key={value} onClick={() => toggleFilter(value)}>
                        <CheckboxButton
                            checked={(filter && filter.has(value)) || false}
                        />
                        {value} ({count})
                    </MenuItem>
                ))}
            </Menu>
        </>
    );
}

ColumnFilter.propTypes = {
    name: PropTypes.string,
    values: PropTypes.arrayOf(PropTypes.object),
    filter: PropTypes.object,
    toggleFilter: PropTypes.func,
    resetFilter: PropTypes.func,
    textButton: PropTypes.bool,
};

function TextButton(props) {
    return (
        <span {...props} style={{ fontWeight: "bold" }}>
            {props.title}
            {props.color && " *"}
        </span>
    );
}
TextButton.propTypes = {
    title: PropTypes.string,
    color: PropTypes.string,
};

function CellValue({ row, column }) {
    const { name } = column,
        value = row[name];

    return <>{value}</>;
}

CellValue.propTypes = {
    row: PropTypes.object,
    column: PropTypes.object,
};

function CellLink({ row, column, nav }) {
    const { name } = column,
        value = row[name],
        { IconButton } = useComponents();
    return (
        <IconButton
            icon="view"
            size="small"
            color="primary"
            onClick={() => nav(value)}
            title={`View ${name} ${value}`}
        />
    );
}

CellLink.propTypes = {
    row: PropTypes.object,
    column: PropTypes.object,
    nav: PropTypes.func,
};

function matchFilters(obj, filters) {
    let match = true;
    Object.entries(filters).forEach(([key, filterValues]) => {
        if (!filterValues.has(obj[key])) {
            match = false;
        }
    });
    return match;
}

function sort(val1, val2, dir = "asc") {
    if (dir == "desc") {
        return sort(val2, val1);
    }
    if (val1 !== undefined && val2 === undefined) {
        return -1;
    } else if (val1 === undefined && val2 !== undefined) {
        return 1;
    } else if (val1 < val2) {
        return -1;
    } else if (val1 > val2) {
        return 1;
    } else {
        return 0;
    }
}
