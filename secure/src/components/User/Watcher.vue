<template>
<div id="watcher" class="ui segment stacked">
    <div class="ui pointing secondary menu dynamic">
        <a class="item active" data-tab='mission'>当前任务</a>
    </div>
    <div v-for="task in tasks">
        <task :task="task"></task>
    </div>
</div>
</template>
<script>
// ####################看守人部分
import ajax from '../../utils/ajax.js'
import task from '../mission/task'
export default {
  name: 'watcher',
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
        }.bind(this))
  },
  components:{
    task
  }
}
</script>
