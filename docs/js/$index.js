---
layout: null
---

import wq, { modules } from 'https://unpkg.com/wq';
import markdown, { components } from 'https://unpkg.com/@wq/markdown@next';
import analyst from 'https://unpkg.com/@wq/analyst';

import Demo from './demo.js';

const React = modules['react'];
const { Typography, Link } = modules['@wq/material'];

components.code = Demo;

wq.use([markdown, analyst]);

const config = {
    site_title: 'Django REST Pandas',
    logo: '/images/icons/django-rest-pandas.svg',
    store: {
        service: '',
        defaults: {
            format: 'json',
        },
    },
    markdown: {
        getEditUrl({ page_config, item_id }) {
            return `https://github.com/wq/django-rest-pandas/edit/main/docs/${page_config.url}/${item_id}.md`;
        },
        getNewUrl({ page_config }) {
            return `https://github.com/wq/django-rest-pandas/new/main/docs/${page_config.url}`;
        },
    },
    material: {
        theme: {
            primary: '#00723f',
            secondary: '#c3ff00',
        }
    },
    pages: {
        {% for page in site.pages %}{% if page.wq_config %}
        {{ page.wq_config.name }}: pageConf({{ page || jsonify }}),{% endif %}{% endfor %}
    }
};

function pageConf(page) {
    if (page.dir === '/') {
        return {
            verbose_name: page.title,
            icon: page.wq_config.icon_data ? page.wq_config.name : null,
            markdown: page.content,
            ...page.wq_config,
        };
    } else {
        return {
            verbose_name_plural: page.title,
            icon: page.wq_config.icon_data ? page.wq_config.name : null,
            markdown: page.content,
            list: true,
            form: [],
            cache: 'all',
            can_change: false,
            can_add: false,
            ordering: ['order', 'title'],
            ...page.wq_config,
        };
    }
}

const ICONS = {
    pin: 'M16,12V4H17V2H7V4H8V12L6,14V16H11.2V22H12.8V16H18V14L16,12Z',
};

wq.use({
    icons: makeIcons(),
    components: {
        Footer() {
            return React.createElement(
                'div',
                {
                    style: {
                        height: '3em',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        backgroundColor: 'white',
                        borderTop: '1px solid rgba(0, 0, 0, 0.12)',
                    },
                },
                React.createElement(
                    Typography,
                    { variant: 'caption', color: 'textSecondary' },
                    [
                        '© 2012-2022 by ',
                        React.createElement(
                            Link,
                            {
                                component: 'a',
                                href: 'https://andrewsheppard.net',
                                target: '_blank',
                            },
                            'S. Andrew Sheppard'
                        ),
                    ]
                )
            );
        },
    },
    start() {
        document.getElementById('content').remove();
    },
    context(ctx, routeInfo) {
        if (routeInfo.page_config.autoindex === false) {
            return { autoindex: false };
        }
    },
    thunks: {
        RENDER() {
            if (location.hash) {
                const el = document.getElementById(location.hash.slice(1));
                if (el) {
                    el.scrollIntoView();
                }
            }
        },
    },
});

function Icon({ data }) {
    return React.createElement(
        'svg',
        { viewBox: '0 0 24 24', style: { width: 24, height: 24 } },
        React.createElement('path', { fill: 'currentColor', d: data })
    );
}

function makeIcons() {
    const icons = {};

    Object.entries(ICONS).forEach(makeIcon);
    Object.entries(config.pages).forEach(([name, conf]) => {
        if (conf.icon_data) {
            makeIcon([name, conf.icon_data]);
        }
    });

    function makeIcon([name, data]) {
        icons[name] = () => React.createElement(Icon, { data });
        icons[name].displayName =
            name[0].toUpperCase() + name.slice(1) + 'Icon';
    }

    return icons;
}

wq.use({
    async ajax(url, formdata, method) {
        if (method === 'POST') {
            return;
        }
        url = url.replace('.json', '/$index.json');
        const response = await fetch(url),
            data = await response.json();
        if (Array.isArray(data)) {
            return data.map(processPage);
        }
        return data;
    },
});

function processPage(page) {
    page.id = page.name.replace('.md', '');
    page.label = page.title = page.title.replace('&amp;', '&');
    page.icon = page.icon || null;
    page.order = page.order || 0;
    page.markdown = page.content;
    delete page.content;

    if (page.module) {
        page.tags = [
            {
                label: page.module,
                color: page.module.startsWith('@wq/') ? 'primary' : 'secondary',
            },
        ];
    } else if (page.tag) {
        page.tags = [
            {
                label: page.tag,
                color: page.tag_color || 'primary',
            },
        ];
    } else {
        page.tags = null;
    }
    return page;
}

wq.init(config).then(wq.prefetchAll);
