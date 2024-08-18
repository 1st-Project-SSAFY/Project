const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true
})

module.exports = {
  devServer: {
    proxy: {
      '/api': {
        target: 'http://3.36.55.201:8000',
        changeOrigin: true,
        pathRewrite: { '^/api': '' },
      },
    },
  },
};
