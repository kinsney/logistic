<template>
<div class="task">
    <h4 class="header ui orange block top attached">任务开始时间：{{ mission.time_start}}</h4>
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
                                <td>{{ mission.car.license }}</td>
                            </tr>
                            <tr>
                                <td>司机：</td>
                                <td>
                                    <h4 class="ui image header">
                                        <img :src="mission.driver.avatar" class="ui mini rounded image">
                                        <div class="content">{{ mission.driver.name }}</div>
                                        <div class="description">工号：{{ mission.driver.workerId }}</div>
                                    </h4>
                                </td>
                            </tr>
                            <tr>
                                <td>押送员：</td>
                                <td>
                                    <h4 class="ui image header" v-for="guarder in mission.guarders">
                                        <img :src="guarder.avatar" class="ui mini rounded image">
                                        <div class="content">{{ guarder.name }}</div>
                                        <div class="description">工号：{{ guarder.workerId }}</div>
                                    </h4>
                                </td>
                            </tr>
                            <tr>
                                <td>目的地：</td>
                                <td>
                                    <h4 class="ui header" v-for="task in mission.tasksInfo">
                                        <i class='ui icon building outline'></i>
                                        <div class="content">{{ task.origin }}</div>
                                    </h4>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
            <div class="eleven wide column">
                <div class="ui segment">
                    <div class="ui steps orderd mini stackable attached ">
                        <div :class="['step',{active: current == index,completed:current>index}]" :data="index" v-for="(task,index) in mission.tasksInfo">
                            <i class="truck icon"></i>
                            <div class="content">
                              <div class="title">{{ desName(task.origin,1) }}</div>
                              <div class="description">{{ desName(task.origin,0) }}</div>
                            </div>
                        </div>
                    </div>
                    <div class="ui attached segment panel">
                        <div v-for="(task,index) in mission.tasksInfo" v-if="current == index">
                            <div class="ui form">
                                <h4 class="ui dividing header">车上的箱子：</h4>
                                <div class="inline field" v-for="container in containers">
                                    <div class="ui checkbox" >
                                        <input type="checkbox" tabindex="0" class="hidden">
                                        <label>箱子编号：{{ container }}</label>
                                    </div>
                                </div>
                                <div class="two fields">
                                    <div class="field">
                                        <h4 class="ui dividing header">需要装箱：</h4>
                                        <div class="inline field" v-for="container in task.load_containers">
                                            <div class="ui checkbox" >
                                                <input type="checkbox" tabindex="0" class="hidden">
                                                <label>箱子编号：{{ container }}</label>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="field">
                                        <h4 class="ui dividing header">需要卸箱：</h4>
                                        <div class="inline field" v-for="container in task.unload_containers">
                                            <div class="ui checkbox" >
                                                <input type="checkbox" tabindex="0" class="hidden">
                                                <label>箱子编号：{{ container }}</label>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div class="inline field">
                                    <div class="ui button  primary " @click="update">
                                        确认
                                    </div>
                                    <div class="ui button right floated negative button">
                                        报警
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div v-if="current==steps">
                            <div class="ui success message visible" >
                              <div class="header">该任务已完成</div>
                              <p>该车辆已完成押送货物及回收货物</p>
                            </div>
                        </div>
                    </div>
                </div>
                <div>
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
  name: 'taskOut',
  data () {
    return {
        current:0,
        update_port:'/task/update_task_driver',
        containers:[],
        openDevice:false
    }
  },
  computed:{
    steps:function(){
        return this.mission.tasksInfo.length
    }
  },
  props:['mission',"port","userInfo"],
  methods : {
    desName (value,index){
        return value.split('-')[index]
    },
    nextStep (){
        let i = this.current
        let load = this.mission.tasksInfo[i].load_containers
        let unload = this.mission.tasksInfo[i].unload_containers
        this.containers = this.containers.concat(load).filter((item) => !(unload.indexOf(item)>=0))
       this.current = this.current+1
    },
    update(){
        let port = this.port + this.update_port
        let phone = this.userInfo.phone
        let task_pk = this.mission.tasksInfo[this.current].task_pk
        let data = {"phone":phone,"task_pk":task_pk}
        ajax.post(port,data).then(function(data){
             this.nextStep()
        }.bind(this))
    },
    start(){

    }
  },
  watch:{
  },
  mounted:function(){
    $('.ui.checkbox').checkbox()
    $('.ui.accordion')
  .accordion()
;
    this.current = this.mission.current_task
    for(var i=0;i<this.current;i++){
        let load = this.mission.tasksInfo[i].load_containers
        let unload = this.mission.tasksInfo[i].unload_containers
        this.containers = this.containers.concat(load).filter((item) => !(unload.indexOf(item)>=0));
    }
  }
}
</script>
