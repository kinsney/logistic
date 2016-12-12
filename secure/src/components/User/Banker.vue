<template>
<div id="banker" class="ui segment stacked">
    <div class="ui pointing secondary menu dynamic">
        <a class="item active" data-tab='mission'>当前任务</a>
    </div>
    <div class="ui tab" data-tab='mission'>
      <div v-for="task in tasks" data-tab='mission'>
        <bankjob :task="task" :port="port" :userInfo="userInfo"></bankjob>
      </div>
    </div>
</div>
</template>
<script>
// ####################银行管理员部分
import ajax from '../../utils/ajax.js'
import bankjob from '../mission/bankjob'
export default {
  name: 'banker',
  data () {
    return {
        misson_port:"/task/get_mission_watcher",
        tasks:[]
    }
  },
  props:['userInfo','port'],
  methods : {
  },
  mounted:function(){
    $('.menu .item').tab('change tab','mission');
    let port = this.port + this.misson_port
    let userInfo = this.userInfo
    ajax.post(port,userInfo).then(function(data){
             this.tasks = data
        }.bind(this))
  },
  components:{
    bankjob
  }
}
</script>
