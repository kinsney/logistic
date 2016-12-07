<template>
<div id="guarder" class="ui segment stacked">
    <div class="ui pointing secondary menu dynamic">
        <a class="item active" data-tab='mission'>当前任务</a>
    </div>
    <div v-for="mission in missions">
        <mission :mission="mission"></mission>
    </div>
</div>
</template>
<script>
// ####################押解员部分
import ajax from '../../utils/ajax.js'
import mission from '../mission/mission'
export default {
  name: 'guarder',
  data () {
    return {
        misson_port:"/task/get_mission_driver",
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
    mission
  }
}
</script>
