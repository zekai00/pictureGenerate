const { defineConfig } = require('@vue/cli-service')

module.exports = defineConfig({
  productionSourceMap: false,
  publicPath: './',
  outputDir: 'dist',
  assetsDir: 'assets',
  devServer: {
      port: 1024,
      host: '0.0.0.0',
      https: false,
      open: true,
      proxy: {
        '/api': {
          target: 'http://10.177.58.143:8000',
          ws: true,
          changeOrigin: true,
          pathRewrite: {
            '^/api': ''
          }
        },
  },

}})
