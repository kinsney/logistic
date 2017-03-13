require('./check-versions')()
var config = require('../config')
if (!process.env.NODE_ENV) process.env.NODE_ENV = JSON.parse(config.dev.env.NODE_ENV)
var path = require('path')
var express = require('express')
var webpack = require('webpack')
var http = require('http')
var url = require('url')
var ws = require('ws');
var opn = require('opn')
var proxyMiddleware = require('http-proxy-middleware')
var webpackConfig = require('./webpack.dev.conf')

// default port where dev server listens for incoming traffic
var port = process.env.PORT || config.dev.port
// Define HTTP proxies to your custom API backend
// https://github.com/chimurai/http-proxy-middleware
var proxyTable = config.dev.proxyTable

var app = express()
var compiler = webpack(webpackConfig)

var devMiddleware = require('webpack-dev-middleware')(compiler, {
  publicPath: webpackConfig.output.publicPath,
  stats: {
    colors: true,
    chunks: false
  }
})

var hotMiddleware = require('webpack-hot-middleware')(compiler)
// force page reload when html-webpack-plugin template changes
compiler.plugin('compilation', function (compilation) {
  compilation.plugin('html-webpack-plugin-after-emit', function (data, cb) {
    hotMiddleware.publish({ action: 'reload' })
    cb()
  })
})

// proxy api requests
Object.keys(proxyTable).forEach(function (context) {
  var options = proxyTable[context]
  if (typeof options === 'string') {
    options = { target: options }
  }
  app.use(proxyMiddleware(context, options))
})

// handle fallback for HTML5 history API
app.use(require('connect-history-api-fallback')())

// serve webpack bundle output
app.use(devMiddleware)

// enable hot-reload and state-preserving
// compilation error display
app.use(hotMiddleware)

// serve pure static assets
var staticPath = path.posix.join(config.dev.assetsPublicPath, config.dev.assetsSubDirectory)
app.use(staticPath, express.static('./static'))

var WebSocketServer = ws.Server
wss = new WebSocketServer({port:5000});

wss.on("connection", function(socket) {
    socket.on("message", function(msg) {
        wss.clients.forEach(function(client) {
          if(client!=socket&&client.readyState===1){
            client.send(msg)
          }
        });
    });
});
// 5号输入口 按钮
// var devicePort = "http://192.168.1.77"
// var buttonWs = new WebSocketServer({port:4001})
// buttonWs.on('connection',function(socket){
//     var button = devicePort + "/ecmd?pin get PA4"
//     setInterval(function(){
//         http.get(url.parse(button),function(res){
//         res.on('data',function(chunk){
//           buttonWs.clients.forEach(function(client) {
//             client.send(chunk.toString())
//           });
//           })
//         })
//     },500)
// })
// // 6号输入口 门信号
// var doorWs = new WebSocketServer({port:4002})
// doorWs.on('connection',function(socket){
//     var door = devicePort + "ecmd?pin get PA5"
//     setInterval(function(){
//         http.get(url.parse(door),function(res){
//         res.on('data',function(chunk){
//           doorWs.clients.forEach(function(client) {
//             client.send(chunk.toString())
//           });
//           })
//         })
//     },500)
// })
// // 7号输入口 1。2门信号
// var frontWs = new WebSocketServer({port:4003})
// frontWs.on('connection',function(socket){
//     var frontDoor = devicePort + "/ecmd?pin get PA6"
//     setInterval(function(){
//         http.get(url.parse(frontDoor),function(res){
//         res.on('data',function(chunk){
//           frontWs.clients.forEach(function(client) {
//             client.send(chunk.toString())
//           });
//           })
//         })
//     },500)
// })

// // 8号输入口 3、4门信号
// var backWs = new WebSocketServer({port:4004})
// backWs.on('connection',function(socket){
//     var backDoor = devicePort + "/ecmd?pin get PA7"
//     setInterval(function(){
//         http.get(url.parse(backDoor),function(res){
//         res.on('data',function(chunk){
//           backWs.clients.forEach(function(client) {
//             client.send(chunk.toString())
//           });
//           })
//         })
//     },500)
// })



module.exports = app.listen(port, function (err) {
  if (err) {
    console.log(err)
    return
  }
  var uri = 'http://localhost:' + port
  console.log('Listening at ' + uri + '\n')

  // when env is testing, don't need open it
  if (process.env.NODE_ENV !== 'testing') {
    opn(uri)
  }
})
