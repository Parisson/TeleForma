const path = require("path");
const outputDir = '../static/teleforma/dist';


module.exports = {
    // publicPath: 'http://172.24.104.152:3000/',
    css: {
        sourceMap: true
    },
    configureWebpack: {
        devServer: {
            host: "npm3000.dockdev.pilotsystems.net",
            public: "https://npm3000.dockdev.pilotsystems.net",
            https: false,
            port: 3000,
            headers: {
                'Access-Control-Allow-Origin': '*'
            },
            disableHostCheck: true
        },
        output: {
            filename: 'app.js',
        },
        
    },
    outputDir: outputDir,
    chainWebpack: config => {
        config
            .entry("app")
            .clear()
            .add("./js/main.ts")
            .end();
        config.resolve.alias
            .set("@", path.join(__dirname, "./js"));
        config.externals({
            ...config.get('externals'),
            jquery: 'jQuery',
            $: 'jQuery'
        });
        if (config.plugins.has("extract-css")) {
            const extractCSSPlugin = config.plugin("extract-css");
            extractCSSPlugin &&
                extractCSSPlugin.tap(() => [{
                    filename: "[name].css",
                }]);
        }
        config.optimization.delete('splitChunks');
        config.plugins
            .delete("html")
            .delete("prefetch")
            .delete("preload");
    }
}