import React, { useState } from "react";
import { Menu, MenuItem, useMediaQuery } from "@mui/material";
import { useComponents } from "@wq/react";
import PropTypes from "prop-types";

export default function AnalystDownload({ url, title, formats }) {
    const [anchorEl, setAnchorEl] = useState(null),
        { Button, IconButton, HorizontalView, Typography, View } =
            useComponents(),
        mobile = useMediaQuery((theme) => theme.breakpoints.down("md")),
        DownloadButton = mobile ? IconButton : Button,
        menuId = "analyst-download",
        currentUrl = new URL(url, window.location.href),
        baseUrl = currentUrl.pathname.replace(/\.[^.]+$/, ""),
        params = currentUrl.search;
    return (
        <>
            <HorizontalView>
                {title ? (
                    <Typography variant="h5">{title}</Typography>
                ) : (
                    <View />
                )}
                <DownloadButton
                    aria-controls={menuId}
                    onClick={(evt) => setAnchorEl(evt.target)}
                    icon="download"
                    variant="contained"
                    color="primary"
                    title="Download Data"
                >
                    Download Data
                </DownloadButton>
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
                        href={`${baseUrl}.${format}${params}`}
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
