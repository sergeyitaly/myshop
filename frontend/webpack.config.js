const path = require("path");

module.exports = {
  entry: [
    'react-hot-loader/patch',
    './frontend/src/main.tsx' // Update the entry point here
  ],
  output: {
    path: path.resolve(__dirname, "./static/frontend"),
    filename: "main.js"
  },
  resolve: {
    extensions: ['.ts', '.tsx', '.js', '.jsx'],
  },
  module: {
    rules: [
      {
        test: /\.(js|jsx|ts|tsx)$/,
        use: 'babel-loader',
        exclude: /node_modules/
      },
      {
        test: /\.s[ac]ss$/i,
        use: [
          "style-loader",
          "css-loader",
          "sass-loader",
        ],
      },
      {
        test: /\.css$/,
        use: ["style-loader", "css-loader"]
      },
      {
        test: /\.(jpg|jpeg|png|gif|mp3|svg)$/,
        use: ["file-loader"]
      },
    ],
  },
  devServer: {
    'static': {
      directory: path.join(__dirname, 'dist'),
    }
  },
  optimization: {
    minimize: true,
  },
};
