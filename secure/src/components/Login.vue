<template>
    <div class="login ui middle aligned center aligned grid">
      <div class="column" style="max-width:450px">
        <h2 class="ui teal image header">
          <div class="content">
            登录
          </div>
        </h2>
        <form class="ui large form">
          <div class="ui stacked segment">
            <div class="field">
              <div class="ui left icon input">
                <i class="user icon"></i>
                <input type="text"  v-model="username" placeholder="手机号">
              </div>
            </div>
            <div class="field">
              <div class="ui left icon input">
                <i class="lock icon"></i>
                <input type="password"  v-model="password" placeholder="密码">
              </div>
            </div>
            <button class="ui fluid large teal submit button" type="submit" @click="login" >登录</button>
          </div>
        </form>
      </div>
    </div>
</template>
<script>
import ajax from '../utils/ajax.js'
export default {
  name: 'login',
  data () {
    return {
      login_port:'/worker/csrf_login',
      username:'',
      password:'',
    }
  },
  props:['userInfo','port'],
  methods : {
    login (event) {
        event.preventDefault()
        let port = this.port + this.login_port
        let username = this.username
        let password = this.password
        let data = {"username":username,"password":password}
        ajax.init('csrftoken')
        let csrftoken = ajax._csrfToken
        ajax.post(port,data).then(function(data){
             this.$emit('finishLogin',data)
        }.bind(this))
    }
  }
}
</script>
<style scoped>
    #login{
    }
</style>
