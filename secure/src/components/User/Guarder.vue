<template>
<div id="guarder" class="ui segment stacked">
    <div class="ui pointing secondary menu dynamic">
        <a class="item active" data-tab='mission'>当前任务</a>
    </div>
    <div v-for="mission in missions">
        <task :mission="mission"></task>
    </div>
</div>
</template>
<script>
// ####################押解员部分
import ajax from '../../utils/ajax.js'
import task from '../mission/task'
export default {
  name: 'guarder',
  data () {
    return {
        misson_port:"/task/get_mission",
        missions:[]
    }
  },
  props:['userInfo',"port"],
  methods : {

  },
  mounted:function(){
    let port = this.port + this.misson_port
    let userInfo = this.userInfo
    ajax.post(port,userInfo).then(function(data){
             this.missions = data
        }.bind(this))

  },
  components:{
    task
  }
}
</script>
