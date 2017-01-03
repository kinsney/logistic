<template>
<div id="banker" class="ui segment stacked">
    <div class="ui pointing secondary menu">
        <a class="item" data-tab='mission'>当前任务</a>
        <div class="right menu">
          <a class="ui button black basic" :href="port+'/container/container'" style="margin-bottom:2px">查看货箱</a>
        </div>
    </div>
    <div class="ui tab" data-tab='mission'>
      <div v-for="(task,index) in tasks" data-tab='mission'>
        <bankjob :task="task" :port="port" :userInfo="userInfo" :bankjobId="index"></bankjob>
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

    let port = this.port + this.misson_port
    let userInfo = this.userInfo
    ajax.post(port,userInfo).then(function(data){
             this.tasks = data
        }.bind(this)).then(function(){
          $('.menu .item').tab('change tab','mission');
        })
  },
  components:{
    bankjob
  }
}
</script>
