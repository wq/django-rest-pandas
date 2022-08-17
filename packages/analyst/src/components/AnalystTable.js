import React, { useEffect, useState, useMemo } from 'react';
import Badge from '@material-ui/core/Badge';
import Menu from '@material-ui/core/Menu';
import MenuItem from '@material-ui/core/MenuItem';
import { get as getPandasCsv } from '@wq/pandas';
import { useComponents } from '@wq/react';
import PropTypes from 'prop-types';

export default function AnalystTable({
    url,
    initial_rows,
    initial_order,
    id_column,
    id_url_prefix,
}) {
    const [data, setData] = useState(),
        [columns, setColumns] = useState(),
        [filters, setFilters] = useState({}),
        [orders, setOrders] = useState(initial_order || {}),
        [rowsPerPage, setRowsPerPage] = useState(initial_rows || 50),
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
        } = useComponents();

    useEffect(() => {
        async function loadData() {
            const data = await getPandasCsv(url, { flatten: true });
            setData(data);
        }
        loadData();
    }, [url]);

    useEffect(() => {
        if (!data || data.length === 0) {
            return;
        }
        const nextColumns = Object.keys(data[0]).map((key) => {
            const metaKeys = {},
                colFilters = { ...filters };
            delete colFilters[key];
            data.datasets.forEach((dataset) => {
                if (!matchFilters(dataset, colFilters)) {
                    return;
                }
                Object.entries(dataset).forEach(([key, value]) => {
                    if (key === 'data') {
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
            if (key === id_column) {
                colInfo.url_prefix = id_url_prefix;
            } else if (metaKeys[key]) {
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
        return sortedData.slice(
            page * rowsPerPage,
            page * rowsPerPage + rowsPerPage
        );
    }, [sortedData, page, rowsPerPage]);

    const toggleOrder = (name) => {
        let nextOrders = { ...orders };
        if (!orders[name]) {
            nextOrders = {
                [name]: 'asc',
                ...nextOrders,
            };
        } else if (orders[name] === 'asc') {
            nextOrders[name] = 'desc';
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
        <TableContainer>
            <Table>
                <TableHead>
                    <TableRow>
                        {columns.map((column) =>
                            column.url_prefix ? (
                                <TableTitle key={column.name} />
                            ) : (
                                <TableTitle key={column.name}>
                                    <div
                                        style={{
                                            display: 'flex',
                                            alignItems: 'center',
                                            marginLeft: -8,
                                            borderLeft: '2px solid #ccc',
                                            paddingLeft: 8,
                                            marginRight: -16,
                                        }}
                                    >
                                        <span
                                            style={{
                                                flex: 1,
                                                fontWeight: 'bold',
                                            }}
                                        >
                                            {column.name}
                                        </span>
                                        <Badge
                                            overlap="circular"
                                            badgeContent={
                                                Object.keys(orders).indexOf(
                                                    column.name
                                                ) + 1
                                            }
                                        >
                                            <IconButton
                                                size="small"
                                                icon={
                                                    orders[column.name] ===
                                                    'desc'
                                                        ? 'sort-desc'
                                                        : orders[column.name]
                                                        ? 'sort-asc'
                                                        : 'sort-none'
                                                }
                                                color={
                                                    orders[column.name] &&
                                                    'secondary'
                                                }
                                                onClick={() =>
                                                    toggleOrder(column.name)
                                                }
                                            />
                                        </Badge>
                                        {column.values && (
                                            <ColumnFilter
                                                {...column}
                                                filter={filters[column.name]}
                                                toggleFilter={(value) =>
                                                    toggleFilter(
                                                        column.name,
                                                        value
                                                    )
                                                }
                                                resetFilter={() =>
                                                    resetFilter(column.name)
                                                }
                                            />
                                        )}
                                    </div>
                                </TableTitle>
                            )
                        )}
                    </TableRow>
                </TableHead>
                <TableBody>
                    {slicedData.map((row, i) => (
                        <TableRow key={i}>
                            {columns.map((column) => (
                                <TableCell key={column.name}>
                                    <CellValue column={column} row={row} />
                                </TableCell>
                            ))}
                        </TableRow>
                    ))}
                </TableBody>
            </Table>
            <TablePagination
                component="div"
                count={sortedData.length}
                page={page}
                rowsPerPage={rowsPerPage}
                onChangePage={(evt, page) => setPage(page)}
                onChangeRowsPerPage={(evt) => setRowsPerPage(evt.target.value)}
            />
        </TableContainer>
    );
}

AnalystTable.propTypes = {
    url: PropTypes.string,
    initial_rows: PropTypes.number,
    initial_order: PropTypes.object,
    id_column: PropTypes.string,
    id_url_prefix: PropTypes.string,
};

function ColumnFilter({ name, values, filter, toggleFilter, resetFilter }) {
    const [anchorEl, setAnchorEl] = useState(null),
        { IconButton, CheckboxButton } = useComponents(),
        menuId = `${name}-menu`;
    return (
        <>
            <IconButton
                aria-controls={menuId}
                onClick={(evt) => setAnchorEl(evt.target)}
                size="small"
                icon="filter"
                color={filter && 'secondary'}
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
};

function CellValue({ row, column }) {
    const { name, url_prefix } = column,
        value = row[name];

    if (url_prefix) {
        return <CellLink row={row} column={column} />;
    } else {
        return <>{value}</>;
    }
}

CellValue.propTypes = {
    row: PropTypes.object,
    column: PropTypes.object,
};

function CellLink({ row, column }) {
    const { name, url_prefix } = column,
        value = row[name],
        { IconButton } = useComponents();
    return (
        <IconButton
            icon="view"
            size="small"
            color="primary"
            component="a"
            href={`${url_prefix}${value}`}
            title={`View ${name} ${value}`}
        />
    );
}

CellLink.propTypes = {
    row: PropTypes.object,
    column: PropTypes.object,
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

function sort(val1, val2, dir = 'asc') {
    if (dir == 'desc') {
        return sort(val2, val1);
    }
    if (val1 < val2) {
        return -1;
    } else if (val1 > val2) {
        return 1;
    } else {
        return 0;
    }
}
