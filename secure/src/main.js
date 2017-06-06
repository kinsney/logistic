import Vue from 'vue'
import App from './App'

/* eslint-disable no-new */

window.vm = new Vue({
  data:{
    devicePort:"http://192.168.0.77",
    remote:"120.27.118.166",
    websocket:"120.27.118.166:3330/websocket"
  },
  el: '#app',
  template: '<App/>',
  components: { App }
})

