import React from 'react';
import { useComponents, useRouteInfo } from '@wq/react';

export default function Analyst() {
    const {
            View,
            Text,
            ScrollView,
            AnalystDownload,
            Typography,
            AnalystTable,
        } = useComponents(),
        {
            page_config: { name, analyst },
        } = useRouteInfo();
    if (!analyst || !analyst.url) {
        return (
            <View>
                <Text>
                    The config for &quot;{name}&quot; should include an
                    `analyst.url` property.
                </Text>
            </View>
        );
    }
    const {
        url,
        title,
        formats,
        initial_rows,
        initial_order,
        id_column,
        id_url_prefix,
    } = analyst;
    return (
        <ScrollView>
            {formats && (
                <AnalystDownload url={url} title={title} formats={formats} />
            )}
            {!formats && title && <Typography variant="h5">{title}</Typography>}
            <AnalystTable
                url={url}
                initial_rows={initial_rows}
                initial_order={initial_order}
                id_column={id_column}
                id_url_prefix={id_url_prefix}
            />
        </ScrollView>
    );
}
