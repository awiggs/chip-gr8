const withLess = require('@zeit/next-less')
const Vars     = require('./Vars');

module.exports = withLess({
    assetPrefix: Vars.sitePrefix,
    webpackDevMiddleware(config) {
        config.watchOptions = {
            ignored: [
                /\.git\//,
                /\.next\//,
                /deps/,
                /node_modules/,
            ]
        }
        return config;
    },
});