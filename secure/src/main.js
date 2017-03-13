import Vue from 'vue'
import App from './App'

/* eslint-disable no-new */

window.vm = new Vue({
  data:{
    devicePort:"http://192.168.1.77",
    remote:"localhost:7000"
  },
  el: '#app',
  template: '<App/>',
  components: { App }
})

