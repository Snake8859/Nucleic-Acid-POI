const { defineConfig } = require("@vue/cli-service");
module.exports = defineConfig({
  transpileDependencies: true,
  publicPath: process.env.NODE_ENV === 'production' ? '/hs-demo' : '/',
  assetsDir: './static',
  devServer: {
    port:8888
  }
});
