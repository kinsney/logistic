<template>
    <div class="login ui middle aligned center aligned grid">
      <div class="column" style="max-width:450px">
        <h2 class="ui teal image header">
          <div class="content">
            登录
          </div>
        </h2>
        <div class="ui top attached tabular menu">
          <a class="item" data-tab="fingerprint">指纹登录</a>
          <a class="item" data-tab="code">密码登录</a>
        </div>
        <div class="ui bottom attached tab segment" data-tab="fingerprint">
          <div class="ui visible message negative" v-if="errorCode==403">
                <p>无该指纹信息</p>
              </div>
        </div>
        <div class="ui bottom attached tab segment" data-tab="code">
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
              <div class="ui visible message negative" v-if="errorCode==403">
                <p>您的账号密码不正确</p>
              </div>
              <div class="ui visible message negative" v-if="errorCode==400">
                <p>请正确输入您的账号密码</p>
              </div>
              <button class="ui fluid large teal submit button" type="submit" @click="login" >登录</button>
            </div>
          </form>
        </div>
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
      print_port:"/worker/print_login",
      username:'',
      password:'',
      errorCode:'',
      socket:''
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
        ajax.post(port,data).then(function(data){
             this.$emit('finishLogin',data)
        }.bind(this),function(error){
            this.errorCode = error.status
        }.bind(this))
    },
    print_login(){
      let port = this.port + this.print_port
      this.socket = new WebSocket("ws://localhost:6001")
      this.socket.onmessage = function(event){
        let pk = Number(event.data)
        let data = {"pk":pk}
        ajax.post(port,data).then(function(data){
          this.$emit('finishLogin',data)
          this.socket.close()
        }.bind(this),function(error){
          this.errorCode = error.status
        }.bind(this))
      }.bind(this)
    }
  },
  mounted:function(){
    $('.menu .item').tab('change tab','fingerprint');
    this.print_login()
  }
}
</script>
<style scoped>
    #login{
    }
</style>
