const path = require("path");
const { existsSync } = require("fs");

// Set the entrypoint to main.jsx by default, but main.tsx if using TypeScript.
// let main = "./disaster_relief/js/main.jsx";
// let map = "./disaster_relief/js/map.jsx";

// if (existsSync("./disaster_relief/js/main.tsx")) {
//   main = "./disaster_relief/js/main.tsx";
//   map =  "./disaster_relief/js/map.jsx";
// }

module.exports = {
  mode: "development",
  entry: {
    main: "./disaster_relief/js/main.jsx", // Main page entry point
    map: "./disaster_relief/js/map.jsx",  // Map page entry point
  },
  output: {
    path: path.join(__dirname, "/disaster_relief/static/js/"),
    filename: "[name].bundle.js", // Outputs main.bundle.js and map.bundle.js
  },
  devtool: "source-map",
  module: {
    rules: [
      {
        // Test for js or jsx files
        test: /\.jsx?$/,
        // Exclude external modules from loader tests
        exclude: /node_modules/,
        loader: "babel-loader",
        options: {
          presets: ["@babel/preset-env", "@babel/preset-react"],
          plugins: ["@babel/transform-runtime"],
        },
      },
      {
        // Support for TypeScript in optional .ts or .tsx files
        test: /\.tsx?$/,
        use: "ts-loader",
        exclude: /node_modules/,
      },
    ],
  },
  resolve: {
    extensions: [".js", ".jsx", ".ts", ".tsx"],
  },
  
};
