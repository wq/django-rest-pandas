import React from "react";
import { useIcon } from "@wq/react";
import PropTypes from "prop-types";

export default function Icon({ icon }) {
    const Icon = useIcon(icon);
    return Icon ? <Icon /> : icon;
}

Icon.propTypes = { icon: PropTypes.string };

export function labelWithIcon(label, iconName) {
    return (
        <>
            <Icon icon={iconName} /> {label}
        </>
    );
}
