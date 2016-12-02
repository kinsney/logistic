import Vue from 'vue'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-default/index.css'
import App from './App'

/* eslint-disable no-new */
Vue.use(ElementUI)

window.vm = new Vue({
  el: '#app',
  template: '<App/>',
  components: { App }
})

