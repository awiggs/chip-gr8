import Head from 'next/head';
import Vars from '../Vars';

// Load Less styles
import './Boot.less';

export default ({ 
    title, 
    keywords    = [], 
    description = '', 
    author      = 'Eric Buss',
    favicon     = '/static/favicon.ico',
}) => (
    <Head>
        <title>{title}</title>
        <meta charSet='UTF-8' />
        <meta name='description' content={description} />
        <meta name='keywords'    content={keywords.join(', ')} />
        <meta name='author'      content={author} />
        <meta name='viewport'    content='width=device-width, initial-scale=1.0' />
        {/* Favicon */}
        <link rel='shortcut icon' href={Vars.sitePrefix + favicon} />
        {/* Static CSS */}
        <link rel='stylesheet' href='/static/css/github.css' />
        <link rel='stylesheet' href='/static/css/spectre.min.css' />
        <link rel='stylesheet' href='/static/css/spectre-exp.min.css' />
        <link rel='stylesheet' href='/static/css/font-awesome.min.css' />
        <link rel='stylesheet' href='/static/css/animate.css' />
        {/* Shimmy */}
        <script src='/static/js/es5-shim.min.js' />
        <script src='/static/js/es6-shim.min.js' />
        <script src='/static/js/object-shim.js' />
    </Head>
);