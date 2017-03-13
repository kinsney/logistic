const electron = require('electron')
// Module to control application life.
const app = electron.app
const { Menu,MenuItem } = electron
// Module to create native browser window.
const BrowserWindow = electron.BrowserWindow
const http = require('http')
const path = require('path')
const url = require('url')
var url = require('url')

// Keep a global reference of the window object, if you don't, the window will
// be closed automatically when the JavaScript object is garbage collected.
let mainWindow
const port = 3000
const remote = 'http://localhost:7000'
const devicePort = "http://192.168.31.77/"

function createWindow () {
  // Create the browser window.
  app.name = "安保系统"
  mainWindow = new BrowserWindow({width: 1200, height: 800})

  // and load the index.html of the app.
  mainWindow.loadURL('http://localhost:'+port)
  const template = [
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
  const menu = Menu.buildFromTemplate(template)
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
var wss = new WebSocketServer({port:5000});
wss.on("connection", function(socket) {
    socket.on("message", function(msg) {
        wss.clients.forEach(function(client) {
          if(client!=socket&&client.readyState===1){
            client.send(msg)
          }
        });
    });
});
main.listen(port)

var deviceWs = new WebSocketServer({port:4000})
deviceWs.on('connection',function(socket){
        setInterval(function(){
        http.get(url.parse(devicePort),function(res){
        res.on('data',function(chunk){
          deviceWs.clients.forEach(function(client) {
            client.send(chunk.toString())
          });
        })
      })
    },200)
})
