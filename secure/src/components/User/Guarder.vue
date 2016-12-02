<template>
<div id="guarder" class="ui segment stacked">
    <div class="ui pointing secondary menu dynamic">
        <a class="item active" data-tab='mission'>当前任务</a>
        <a class="item" data-tab='container'>货箱管理</a>
    </div>
    <div data-tab="mission" class="ui tab active">
            {{ mission }}
            {{ userInfo }}
    </div>
    <div data-tab="container" class="ui tab">
    </div>
</div>
</template>
<script>
// ####################押解员部分
import ajax from '../../utils/ajax.js'
export default {
  name: 'guarder',
  data () {
    return {
        wsSocket:{},
        misson_port:"/task/get_misson",
        mission:{}
    }
  },
  props:['userInfo'],
  methods : {

  },
  mounted:function(){
    let port = this.port + this.misson_port
    let userInfo = this.userInfo
    ajax.post(port,userInfo).then(function(data){
             this.mission = data
        }.bind(this))

  }
}
</script>
