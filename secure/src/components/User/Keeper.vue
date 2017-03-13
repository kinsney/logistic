<template>
<div id="keeper" class="ui segment stacked">
    <div class="ui pointing secondary menu dynamic keeper">
        <a class="item" :data-tab="'gunjob'+index" v-for="(gunjob,index) in gunjobs">车辆{{gunjob.car}}</a>
    </div>
    <div class="ui tab" :data-tab="'gunjob'+index" v-for="(gunjob,index) in gunjobs">
      <div v-for="(task,index) in gunjob.info" >
        <gunjob :task="task" :port="port" :userInfo="userInfo" :taskId="index"></gunjob>
      </div>
    </div>
</div>
</template>
<script>
// ####################枪支管理员部分
import ajax from '../../utils/ajax.js'
import task from '../mission/task'
import gunjob from '../mission/gunjob'
export default {
  name: 'keeper',
  data () {
    return {
        mission_port:"/task/get_gunjobs",
        gunjobs:[],
        isLogged:false,
        errorCode:""
    }
  },
  props:['userInfo','port'],
  methods : {
  },
  mounted:function(){

    let port = this.port + this.mission_port
    let userInfo = this.userInfo
    ajax.post(port,userInfo).then(function(data){
             this.gunjobs = data
        }.bind(this)).then(function(){
          $('.keeper .item').tab('change tab','gunjob0');
        })
  },
  components:{
    gunjob
  }
}
</script>
