import React from "react";
import { Formik } from "formik";
import { Grid } from "@mui/material";
import { AutoInput } from "@wq/react";
import { View } from "@wq/material";
import PropTypes from "prop-types";

export default function AnalystForm({ form, options, setOptions }) {
    return (
        <Formik
            initialValues={options}
            enableReinitialize={true}
            validate={setOptions}
        >
            <View sx={{ p: 2 }}>
                <Grid container spacing={1} sx={{}}>
                    {form.map((field) => (
                        <GridInput key={field.name} {...field} />
                    ))}
                </Grid>
            </View>
        </Formik>
    );
}

AnalystForm.propTypes = {
    form: PropTypes.arrayOf(PropTypes.object),
    options: PropTypes.object,
    setOptions: PropTypes.func,
};

function GridInput(props) {
    if (props.type === "hidden") {
        return <AutoInput {...props} />;
    } else if (props.fullwidth) {
        return (
            <Grid item xs={12} lg={6} xl={4}>
                <AutoInput {...props} />
            </Grid>
        );
    } else {
        return (
            <Grid item xs={12} md={6} lg={3} xl={2}>
                <AutoInput {...props} />
            </Grid>
        );
    }
}

GridInput.propTypes = {
    type: PropTypes.string,
    fullwidth: PropTypes.bool,
};
