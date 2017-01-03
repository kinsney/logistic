<template>
<div id="driver" class="ui segment stacked">
    <div class="ui pointing secondary menu dynamic">
        <a class="item" :data-tab="'mission'+index" v-for="(mission,index) in missions" v-if="mission.current_task==mission.tasksInfo.length">任务{{index+1}}（完成）</a>
        <a class="item" :data-tab="'mission'+index" v-for="(mission,index) in missions" v-if="mission.current_task!=mission.tasksInfo.length">任务{{index+1}}</a>
    </div>
    <div v-for="(mission,index) in missions" class="ui tab" :data-tab="'mission'+index">
        <mission :mission="mission" :port="port" :userInfo="userInfo" :missionId="index"></mission>
    </div>
</div>

</template>
<script>
// ####################司机部分
import ajax from '../../utils/ajax.js'
import mission from '../mission/mission'
export default {
  name: 'driver',
  data () {
    return {
        misson_port:"/task/get_mission_driver",
        missions:[],
    }
  },
  props:['userInfo',"port"],
  methods : {

  },
  mounted :function(){
    let userInfo = this.userInfo
    let port = this.port + this.misson_port
    ajax.post(port,userInfo).then(function(data){
             this.missions = data
        }.bind(this)).then(function(){
          $('.menu .item').tab('change tab','mission0');
        })
  },
  components:{
    mission
  }
}
</script>
