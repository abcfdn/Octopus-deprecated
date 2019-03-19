const fs = require('fs');

if (process.env.NODE_ENV === 'development') {
    const devServerConfigPath = 'react-scripts/config/webpackDevServer.config';
    const devServerConfig = require(devServerConfigPath);
    require.cache[require.resolve(devServerConfigPath)].exports = (
      proxy,
      allowedHost
    ) => {
      const conf = devServerConfig(proxy, allowedHost);
      conf.https = {
        key: fs.readFileSync('/root/cert/blockchainabc.org.key'),
        cert: fs.readFileSync('/root/cert/blockchainabc.org.crt')
      };
      return conf;
    };
}

module.exports = function override(config, env) {
  return config;
}
