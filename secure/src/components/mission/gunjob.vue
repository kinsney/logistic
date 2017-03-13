<template>
    <div class="task">
        <h4 class="header ui orange block top attached">任务开始时间：{{taskInfo.time_start}}</h4>
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
                                <td>{{ taskInfo.car.license }}</td>
                            </tr>
                            <tr>
                                <td>司机：</td>
                                <td>
                                    <h4 class="ui image header">
                                        <img :src="taskInfo.driver.avatar" class="ui mini rounded image">
                                        <div class="content">{{ taskInfo.driver.name }}</div>
                                        <div class="description">工号：{{ taskInfo.driver.workerId }}</div>
                                    </h4>
                                </td>
                            </tr>
                            <tr>
                                <td>押送员：</td>
                                <td>
                                    <h4 class="ui image header" v-for="guarder in taskInfo.guarders">
                                        <img :src="guarder.avatar" class="ui mini rounded image">
                                        <div class="content">{{ guarder.name }}</div>
                                        <div class="description">工号：{{ guarder.workerId }}</div>
                                    </h4>
                                </td>
                            </tr>
                            <tr>
                                <td>解款员：</td>
                                <td>
                                    <h4 class="ui image header" v-for="reliver in taskInfo.relivers">
                                        <img :src="reliver.avatar" class="ui mini rounded image">
                                        <div class="content">{{ reliver.name }}</div>
                                        <div class="description">工号：{{ reliver.workerId }}</div>
                                    </h4>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
            <div class="eleven wide column">
                <div class="ui segment" :class="'mission'+taskInfo.mission_pk">
                    <div class="ui steps orderd mini stackable attached ">
                        <div :class="['step',{active:!taskInfo.getGun,completed:taskInfo.getGun}]">
                            <i class="truck icon"></i>
                            <div class="content">
                                <div class="title">
                                    领枪
                                </div>
                            </div>
                        </div>
                        <div class="step" :class="{active:taskInfo.getGun&&!taskInfo.returnGun,completed:taskInfo.returnGun}">
                            <i class="truck icon"></i>
                            <div class="content">
                                <div class="title">
                                    还枪
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="ui success message visible" v-if="taskInfo.getGun&&taskInfo.returnGun" >
                        <div class="header">该任务已完成</div>
                        <p>该任务已完成取枪及还抢</p>
                    </div>
                    <div v-else>
                        <h4 class="ui dividing header">枪支列表</h4>
                        <div class="inline field" v-for="gun in taskInfo.guns">
                            <div class="ui checkbox disabled inCar" :class="gun">
                                <input type="checkbox" tabindex="0" class="hidden" >
                                <label>枪支编号：{{ gun }}</label>
                            </div>
                        </div>
                        <div class="inline field" style="margin-top:20px;">
                            <div class="ui button basic" @click="verify" v-if="!missionStart">
                                已确认身份
                            </div>
                            <div class="ui button primary" @click="update" :class="{disabled:!allchecked}" v-else>
                                确认
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            </div>
        </div>
    </div>
</template>
<script>
import ajax from '../../utils/ajax.js'
export default {
  name: 'task',
  data () {
    return {
        socket:null,
        allchecked:false,
        missionStart:false,
        updatePort:'/task/update_routine',
        taskInfo:null
    }
  },
  computed:{
  },

  props:['task',"port","userInfo"],
  methods : {
    verify(){
        this.missionStart = true
        this.socket = new WebSocket("ws://localhost:5000");
        this.socket.onmessage = function(event){
            let mission = 'mission' + this.taskInfo.mission_pk
            let $checkbox = $('.'+mission).find('.checkbox')
            let allchecked = this.allchecked
            let gunNumber = event.data
            allchecked = true
            $('.'+mission).find('.checkbox.'+gunNumber).checkbox('check')
            $checkbox.each(function(){
                        if(!$(this).checkbox('is checked')){
                            allchecked = false
                        }
                    })
            this.allchecked = allchecked
        }.bind(this)
    },
    update(){
        let port = this.port + this.updatePort
        if(this.taskInfo.getGun){
            let data = {"content":"return","id":this.taskInfo.mission_pk}
            ajax.post(port,data).then(function(data){
                this.taskInfo = data
            }.bind(this))
        }else{
            let data = {"content":'get',"id":this.taskInfo.mission_pk}
            ajax.post(port,data).then(function(data){
                this.taskInfo = data
            }.bind(this))
        }
        this.allchecked = false
        this.missionStart = false
        this.socket.close()
    }
  },
  watch:{
  },
  created:function(){
    this.taskInfo = this.task
  }
}
</script>
