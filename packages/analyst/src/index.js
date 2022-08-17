import * as components from './components/index';
import * as views from './views/index';
import * as icons from './icons';

const analyst = {
    name: 'analyst',
    components: { ...components },
    views: { ...views },
    icons: { ...icons },
};

export default analyst;

export * from './components/index';
export * from './views/index';
