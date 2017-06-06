 <template>
  <div id="app">
    <Login v-on:finishLogin="getUserInfo" :userInfo="userInfo" v-if="!userInfo" :port="port"></Login>
    <UserPanel :userInfo="userInfo" v-if="userInfo" v-on:logout="logout" :port="port"></UserPanel>
  </div>
</template>

<script>

import Login from './components/Login'
import UserPanel from './components/UserPanel'
import 'hammerjs'
import './static/semantic/semantic.min.css'
import './static/semantic/semantic.min.js'
export default {
  name: 'app',
  data () {
    return {
      userInfo:null,
      port:'http://120.27.118.166',
    }
  },
  components: {
    Login,
    UserPanel
  },
  methods : {
    getUserInfo (info) {
      this.userInfo = info
    },
    logout (){
      this.userInfo = null
    }
  }
}
</script>

<style>
#app{
  padding: 20px
}
</style>
