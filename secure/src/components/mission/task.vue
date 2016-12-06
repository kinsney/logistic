<template>
<div clas="task">
    <h4 class="header ui orange block top attached" v-html="mission.time_start"></h4>
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
                                    </h4>
                                </td>
                            </tr>
                            <tr>
                                <td>押送员：</td>
                                <td>
                                    <h4 class="ui image header" v-for="guarder in mission.guarders">
                                        <img :src="guarder.avatar" class="ui mini rounded image">
                                        <div class="content">{{ guarder.name }}</div>
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
                            {{ task }}
                            <div class="ui form">
                                <h4 class="ui dividing header">车上的箱子：</h4>
                                <div class="inline field" v-for="container in containers">
                                    <div class="ui checkbox" >
                                        <input type="checkbox" tabindex="0" class="hidden">
                                        <label>箱子编号：{{ container }}</label>
                                    </div>
                                </div>
                                <h4 class="ui dividing header">需要装箱：</h4>
                                <div class="inline field" v-for="container in task.load_containers">
                                    <div class="ui checkbox" >
                                        <input type="checkbox" tabindex="0" class="hidden">
                                        <label>箱子编号：{{ container }}</label>
                                    </div>
                                </div>
                                <h4 class="ui dividing header">需要卸箱：</h4>
                                <div class="inline field" v-for="container in task.unload_containers">
                                    <div class="ui checkbox" >
                                        <input type="checkbox" tabindex="0" class="hidden">
                                        <label>箱子编号：{{ container }}</label>
                                    </div>
                                </div>
                                <div class="inline field">
                                    <div class="ui button  primary" @click="nextStep">
                                        确认
                                    </div>
                                    <div class="ui button right floated negative button">
                                        报警
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div v-if="current == 'back'">
                            {{mission}}

                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

</template>
<script>
// ####################出勤任务部分
export default {
  name: 'taskOut',
  data () {
    return {
        current:"0",
        containers:[]
    }
  },
  computed:{
    steps:function(){
        return this.mission.tasksInfo.length
    }
  },

  props:['mission'],
  methods : {
    desName (value,index){
        return value.split('-')[index]
    },
    nextStep (){
        let i = Number(this.current)
        let load = this.mission.tasksInfo[i].load_containers
        let unload = this.mission.tasksInfo[i].unload_containers
        this.containers = this.containers.concat(load).filter((item) => !(unload.indexOf(item)>=0))
       this.current = Number(this.current)+1+""
    }
  },
  watch:{
  },
  mounted:function(){
    $('.ui.checkbox').checkbox()
    let index = Number(this.current)
    for(var i=0;i<index;i++){
        let load = this.mission.tasksInfo[i].load_containers
        let unload = this.mission.tasksInfo[i].unload_containers
        this.containers = this.containers.concat(load).filter((item) => (unload.indexOf(item)>=0));
    }

  }
}
</script>
