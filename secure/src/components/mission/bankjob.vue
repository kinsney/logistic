<template>
    <div>
        <h4 class="header ui orange block top attached">任务开始时间：{{task.taskInfo.start_time}}</h4>
        <div class="ui attached segment bottom">
            <div class="ui grid">
                <div class="five wide column">
                    <div class="ui segment">
                        <table class="ui very basic celled table" >
                        <thead>
                            <tr><th colspan="2">任务信息</th></tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>车牌号：</td>
                                <td>{{ task.car.license }}</td>
                            </tr>
                            <tr>
                                <td>司机：</td>
                                <td>
                                    <h4 class="ui image header">
                                        <img :src="task.driver.avatar" class="ui mini rounded image">
                                        <div class="content">{{ task.driver.name }}</div>
                                        <div class="description">
                                            工号：{{ task.driver.workerId}}
                                        </div>
                                    </h4>
                                </td>
                            </tr>
                            <tr>
                                <td>押送员：</td>
                                <td>
                                    <h4 class="ui image header" v-for="guarder in task.guarders">
                                        <img :src="guarder.avatar" class="ui mini rounded image">
                                        <div class="content">{{ guarder.name }}</div>
                                        <div class="description">
                                            工号：{{ guarder.workerId}}
                                        </div>
                                    </h4>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
            <div class="eleven wide column">
                <div class="ui segment">
                    <div class="ui form" :id="'bankjob'+bankjobId">
                        <div class="two fields">
                            <div class="field">
                                <h4 class="ui dividing header">接收货箱</h4>
                                <div class="inline field" v-for="container in task.taskInfo.unload_containers">
                                    <div class="ui checkbox disabled" :class="container" >
                                        <input type="checkbox" tabindex="0" class="hidden">
                                        <label>箱子编号：{{ container }}</label>
                                    </div>
                                </div>
                            </div>
                            <div class="field">
                                <h4 class="ui dividing header">运出货箱</h4>
                                <div class="inline field" v-for="container in task.taskInfo.load_containers">
                                    <div class="ui checkbox disabled" :class="container">
                                        <input type="checkbox" tabindex="0" class="hidden">
                                        <label>箱子编号：{{ container }}</label>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="inline field" v-if="status=='failed'||status=='load'">
                            <div class="ui button basic" @click="start" v-if="!missionStart">
                                任务开始
                            </div>
                            <div class="ui button primary" @click="update" v-if="missionStart" :class="{disabled:!allchecked}" >
                                确认
                            </div>
                            <div class="ui button right floated negative button">
                                报警
                            </div>
                        </div>
                        <div class="ui success message visible" v-else >
                              <div class="header">该任务已完成</div>
                              <p>网点已完成货箱的接收及运出</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
// ####################出勤任务部分
import ajax from '../../utils/ajax.js'
export default {
  name: 'bankjob',
  data () {
    return {
        update_port:'/task/update_task_watcher',
        openDevice:false,
        status:"",
        missionStart:false,
        allchecked:false,
        socket:null,
    }
  },
  computed:{
  },
  props:['task',"port","userInfo","bankjobId"],
  methods : {
    update(){
        let port = this.port + this.update_port
        let phone = this.userInfo.phone
        let task_pk = this.task.taskInfo.task_pk
        let data = {"phone":phone,"task_pk":task_pk}
        ajax.post(port,data).then(function(data){
            this.status = data.status
            this.socket.close()
        }.bind(this))
    },
    start (){
        this.socket = new WebSocket("ws://localhost:5000");
        this.socket.onmessage = function(event){
            if(this.missionStart){
                let bankjob = 'bankjob'+this.bankjobId
                let $checkbox = $('#'+bankjob).find('.checkbox')
                let allchecked = this.allchecked
                let containerNumber = event.data
                allchecked = true
                $('#'+bankjob).find('.checkbox.'+containerNumber).checkbox('check')
                  $checkbox.each(function(){
                        if(!$(this).checkbox('is checked')){
                            allchecked = false
                        }
                    })
                this.allchecked = allchecked
            }
        }.bind(this)
        this.missionStart = true
      }
  },
  watch:{
  },
  mounted:function(){
    $('.ui.checkbox').checkbox()
    this.status = this.task.taskInfo.status
  }
}
</script>
