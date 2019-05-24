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
        <link rel='stylesheet' href={Vars.sitePrefix + '/static/css/github.css'} />
        <link rel='stylesheet' href={Vars.sitePrefix + '/static/css/spectre.min.css'} />
        <link rel='stylesheet' href={Vars.sitePrefix + '/static/css/spectre-exp.min.css'} />
        <link rel='stylesheet' href={Vars.sitePrefix + '/static/css/font-awesome.min.css'} />
        <link rel='stylesheet' href={Vars.sitePrefix + '/static/css/animate.css'} />
        {/* Shimmy */}
        <script src={Vars.sitePrefix + '/static/js/es5-shim.min.js'} />
        <script src={Vars.sitePrefix + '/static/js/es6-shim.min.js'} />
        <script src={Vars.sitePrefix + '/static/js/object-shim.js'} />
    </Head>
);