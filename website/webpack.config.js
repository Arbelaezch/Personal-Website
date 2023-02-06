const path = require('path');

module.exports = {
    entry: './assets/index.js',  // path to our input file
    output: {
        filename: 'index-bundle.js',  // output bundle file name
        path: path.resolve(__dirname, './static'),  // path to our Django static directory
    },
    module: {
        rules: [
        // This tells webpack to use Babel's env and react presets to compile all .js and .jsx files 
        // not in the node_modules directory.
        {
            test: /\.(js|jsx)$/,
            exclude: /node_modules/,
            loader: "babel-loader",
            options: { presets: ["@babel/preset-env", "@babel/preset-react"] }
        },
        ]
    },
};


