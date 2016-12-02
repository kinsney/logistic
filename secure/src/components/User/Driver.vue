<template>
<div id="driver" class="ui segment stacked">
    <div class="ui pointing secondary menu dynamic">
        <a class="item active">当日任务</a>
    </div>
    <div v-for="mission in missions">
        <taskOut :mission="mission"></taskOut>
    </div>
</div>

</template>
<script>
// ####################银行管理员部分
import ajax from '../../utils/ajax.js'
import taskIn from '../mission/taskIn'
import taskOut from '../mission/taskOut'
export default {
  name: 'driver',
  data () {
    return {
        misson_port:"/task/get_mission",
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
        }.bind(this))
  },
  components:{
    taskOut,
    taskIn
  }
}
</script>
