<template>
<div id="guarder" class="ui segment stacked">
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
        }.bind(this)).then(function(){
          $('.menu .item').tab('change tab','mission0');
        })
  },
  components:{
    mission
  }
}
</script>
