import React, { useState } from "react";
import Menu from "@material-ui/core/Menu";
import MenuItem from "@material-ui/core/MenuItem";
import { useComponents } from "@wq/react";
import PropTypes from "prop-types";

export default function AnalystDownload({ url, title, formats }) {
    const [anchorEl, setAnchorEl] = useState(null),
        { Button, HorizontalView, Typography, View } = useComponents(),
        menuId = "analyst-download",
        baseUrl = url.replace(/\.[^.]+$/, "");
    return (
        <>
            <HorizontalView>
                {title ? (
                    <Typography variant="h5">{title}</Typography>
                ) : (
                    <View />
                )}
                <Button
                    aria-controls={menuId}
                    onClick={(evt) => setAnchorEl(evt.target)}
                    icon="download"
                    variant="contained"
                    color="primary"
                >
                    Download Data
                </Button>
            </HorizontalView>
            <Menu
                id={menuId}
                anchorEl={anchorEl}
                open={!!anchorEl}
                onClose={() => setAnchorEl(null)}
            >
                {Object.entries(formats).map(([format, label]) => (
                    <MenuItem
                        key={format}
                        component="a"
                        href={`${baseUrl}.${format}`}
                        target="_blank"
                    >
                        {label}
                    </MenuItem>
                ))}
            </Menu>
        </>
    );
}

AnalystDownload.propTypes = {
    url: PropTypes.string,
    title: PropTypes.string,
    formats: PropTypes.object,
};
