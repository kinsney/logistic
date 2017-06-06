'use strict'
var electron = require('electron')
// Module to control application life.
var app = electron.app
var { Menu,MenuItem } = electron
// Module to create native browser window.
var BrowserWindow = electron.BrowserWindow
var http = require('http')
var path = require('path')
var url = require('url')
// Keep a global reference of the window object, if you don't, the window will
// be closed automatically when the JavaScript object is garbage collected.
var mainWindow
var port = 3000
var devicePort = "http://10.107.2.77"

function createWindow () {
  // Create the browser window.
  app.name = "安保系统"
  mainWindow = new BrowserWindow({width: 1200, height: 800})
mainWindow.webContents.openDevTools()
  // and load the index.html of the app.

var remote = 'http://120.27.118.166'
  mainWindow.loadURL('http://localhost:'+port)
  var template = [
    {
        submenu:[
          {
            label:"退出系统",
            role:"quit"
          }
        ]
    },
    {
      label:"切换系统",
      submenu:[
      {
        label:"进入用户系统",
        click(){
          mainWindow.loadURL('http://localhost:'+port)
        }
      },
      {
        type:'separator'
      },
      {
        label:"进入管理系统",
        click(){
          mainWindow.loadURL(remote)
        }
      },
      {
        type:'separator'
      }
    ]}]
  var menu = Menu.buildFromTemplate(template)
  Menu.setApplicationMenu(menu)

  // Open the DevTools.
  // Emitted when the window is closed.
  mainWindow.on('closed', function () {
    // Dereference the window object, usually you would store windows
    // in an array if your app supports multi windows, this is the time
    // when you should delete the corresponding element.
    mainWindow = null
  })
}

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.on('ready', createWindow)

// Quit when all windows are closed.
app.on('window-all-closed', function () {
  // On OS X it is common for applications and their menu bar
  // to stay active until the user quits explicitly with Cmd + Q
  if (process.platform !== 'darwin') {
    app.quit()
  }
})

app.on('activate', function () {
  // On OS X it's common to re-create a window in the app when the
  // dock icon is clicked and there are no other windows open.
  if (mainWindow === null) {
    createWindow()
  }
})

// In this file you can include the rest of your app's specific main process
// code. You can also put them in separate files and require them here.
var ws = require('ws');
var express = require('express')
var main = express();
main.use(express.static(path.join(__dirname, 'dist')))
var WebSocketServer = ws.Server
main.listen(port)
  var wss = new WebSocketServer({port:5000});
  //RFID
  wss.on("connection", function(socket) {
      socket.on("message", function(msg) {
          wss.clients.forEach(function(client) {
            if(client!=socket&&client.readyState===1){
              client.send(msg)
            }
          });
      });
  });
wss.on('error',function(e){
	console.log(e)
})
//指纹
  var printer = new WebSocketServer({port:6001});
  printer.on("connection", function(socket) {
      socket.on("message", function(msg) {
          printer.clients.forEach(function(client) {
            if(client!=socket&&client.readyState===1){
              client.send(msg)
            }
          });
      });
  });
printer.on('error',function(e){
	console.log(e)
})

// 手持
var handset = new WebSocketServer({port:7001});
handset.on("connection", function(socket) {
    socket.on("message", function(msg) {
        handset.clients.forEach(function(client) {
          if(client!=socket&&client.readyState===1){
            console.log(msg)
            client.send(msg)
          }
        });
    });
});
handset.on('error',function(e){
	console.log(e)
})
// 5号输入口 按钮

var buttonWs = new WebSocketServer({port:4001})
buttonWs.on('connection',function(socket){
    var button = devicePort + "/ecmd?pin get PA6"
    var connection = function(){
        http.get(url.parse(button),function(res){
        res.on('data',function(chunk){
          buttonWs.clients.forEach(function(client) {
            client.send(chunk.toString())
          });
        res.on('end',function(){setTimeout(connection,500)})
          })
        res.on('error',function(){
        	console.log(123)
        })
        }).on('error',function(e){
        	console.log(e)
        })
    }
    connection()
})

// 6号输入口 门信号

var doorWs = new WebSocketServer({port:4002})
doorWs.on('connection',function(socket){
    var door = devicePort + "/ecmd?pin get PA5"
    var connection = function(){
        http.get(url.parse(door),function(res){
        res.on('data',function(chunk){
          doorWs.clients.forEach(function(client) {
            client.send(chunk.toString())
          });
        res.on('end',function(){setTimeout(connection,500)})
          })
        res.on('error',function(){
        	console.log(123)
        })
        }).on('error',function(e){
        	console.log(e)
        })
    }
    connection()
})
// var doorWs = new WebSocketServer({port:4002})
// doorWs.on('connection',function(socket){
//     var door = devicePort + "/ecmd?pin get PA5"
//     setInterval(function(){
//         http.get(url.parse(door),function(res){
//         res.on('data',function(chunk){
//           doorWs.clients.forEach(function(client) {
//             client.send(chunk.toString())
//           });
//           })
//         res.on('error',function(){
//         	console.log(123)
//         })
//         })
//     },500)
// })
// doorWs.on('error',function(e){
// 	console.log(e)
// })
//7号输出口 1。2门信号
var frontWs = new WebSocketServer({port:4003})
frontWs.on('connection',function(socket){
    var frontDoor = devicePort + "/ecmd?pin get PA6"
    var connection = function(){
        http.get(url.parse(frontDoor),function(res){
        res.on('data',function(chunk){
          frontWs.clients.forEach(function(client) {
            client.send(chunk.toString())
          });
        res.on('end',function(){setTimeout(connection,500)})
          })
        res.on('error',function(){
        	console.log(123)
        })
        }).on('error',function(e){
        	console.log(e)
        })
    }
    connection()
})

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
// frontWs.on('error',function(e){
// 	console.log(e)
// })
// // 8号输出口 3、4门信号 门是否关牢
var backWs = new WebSocketServer({port:4004})
backWs.on('connection',function(socket){
    var backDoor = devicePort + "/ecmd?pin get PA5"
    var connection = function(){
        http.get(url.parse(backDoor),function(res){
        res.on('data',function(chunk){
          backWs.clients.forEach(function(client) {
            client.send(chunk.toString())
          });
        res.on('end',function(){setTimeout(connection,500)})
          })
        res.on('error',function(){
        	console.log(123)
        })
        }).on('error',function(e){
        	console.log(e)
        })
    }
    connection()
})
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
// backWs.on('error',function(e){
// 	console.log(e)
// })
