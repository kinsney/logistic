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
                                <td>解款员：</td>
                                <td>
                                    <h4 class="ui image header" v-for="reliver in mission.relivers">
                                        <img :src="reliver.avatar" class="ui mini rounded image">
                                        <div class="content">{{ reliver.name }}</div>
                                        <div class="description">工号：{{ reliver.workerId }}</div>
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
                        <div :class="['step',{active: current == index,completed:task.status=='done'}]" :data="index" v-for="(task,index) in mission.tasksInfo">
                            <i class="truck icon"></i>
                            <div class="content">
                              <div class="title">{{ desName(task.origin,1) }}</div>
                              <div class="description">{{ desName(task.origin,0) }}</div>
                            </div>
                        </div>
                    </div>
                    <div class="ui pointing secondary menu">
                        <a href="#" :class="['step',{active: current == index,completed:task.status=='done'}]" class="item" v-for="(task,index) in mission.tasksInfo" @click="current=index,allchecked=false,missionStart=false,socket=null">
                            {{ desName(task.origin,0) }}
                            <i class="ui checkmark green icon" v-if="task.status=='done'"></i>
                            <i class="ui spinner icon loading" v-else></i>
                        </a>
                    </div>
                    <div class="ui attached segment">
                        <h4 class="ui dividing header">车上的箱子:（{{ mission.containers.length}}）</h4>
                        <div class="inline field" v-for="container in mission.containers">
                            <div class="ui   inCar" :class="container">
                                <label>箱子编号：{{ container }}</label>
                            </div>
                        </div>
                    </div>
                    <div class="ui attached segment panel" >
                        <div v-for="(task,index) in mission.tasksInfo" v-if="current == index">
                            <div class="ui form">
                                <div class="two fields" :class="'mission'+missionId" v-if="task.status=='failed'||task.status=='receive'">
                                    <div class="field">
                                        <h4 class="ui dividing header">需要装箱:（{{task.load_containers.length}}）</h4>
                                        <div class="inline field" v-for="container in task.load_containers">
                                            <div class="ui checkbox disabled" :class="container">
                                                <input type="checkbox" tabindex="0" class="hidden">
                                                <label>箱子编号：{{ container }}</label>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="field">
                                        <h4 class="ui dividing header">需要卸箱:（{{task.unload_containers.length}}）</h4>
                                        <div class="inline field" v-for="container in task.unload_containers">
                                            <div class="ui checkbox disabled" :class="container">
                                                <input type="checkbox" tabindex="0" class="hidden">
                                                <label>箱子编号：{{ container }}</label>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div v-if="task.status=='done'">
                                    <div class="ui success message visible" >
                                        <div class="header">该任务已完成</div>
                                        <p>该车辆已完成押送货物及回收货物</p>
                                    </div>
                                </div>
                                <div class="inline field" v-if="task.status=='failed'||task.status=='receive'">
                                    <div class="ui button basic" @click="missionStart=true" v-if="!missionStart">
                                        任务开始
                                    </div>
                                    <div class="ui button  primary" @click="update" v-else :class="{disabled:!allchecked}">
                                        确认
                                    </div>
                                    <div class="ui button right floated negative button" @click="alert" v-if="!isDanger">
                                        报警
                                    </div>
                                </div>
                            </div>
                            <div class="ui" v-if="task.status=='load'">
                                <div class="ui field" :class="'handset'+missionId">
                                    <h4 class="ui dividing header">需要检验的箱子:（{{task.load_containers.length+task.unload_containers.length}}）</h4>
                                    <div class="inline field" v-for="container in task.unload_containers">
                                        <div class="ui checkbox disabled" :class="container">
                                            <input type="checkbox" tabindex="0" class="hidden">
                                            <label>箱子编号：{{ container }}</label>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                     </div>
                </div>
                <div>
                </div>
            </div>
        </div>
    </div>
<div class="ui modal small" :class="'modal'+mission.mission_pk">
  <div class="ui icon header">
    <i class="alarm red icon"></i>
    紧急报警
  </div>
  <div class="content red" style="text-align:center">
    <p>已向中控发出警报信息,等待中控处理！</p>
  </div>
</div>
<div class="ui modal dooralert">
  <div class="ui icon header">
    <i class="alarm red icon"></i>
    紧急报警
  </div>
  <div class="content red" style="text-align:center">
    <p>门意外开启，请检查！</p>
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
        openDevice:false,
        allchecked:false,//RFID
        socket:null,
        missionStart:false,
        alertSocket:null,
        devicePort:window.vm.devicePort,
        remote:window.vm.remote,
        alertOrNot:false,
        isDanger:false,
        frontDoorLocked:false,
        backDoorLocked:false,
        handset_port:'/task/handset_report',
        handSocket:null,
        allverify:false,//手持机
        checkSocket:null,
        allInCar:false,
        websocket:window.vm.websocket,
        doorOpen:false,
        stack:[],
        plus:[],
        minus:[],
        ratio:2
    }
  },
  props:['mission',"port","userInfo",'missionId'],
  methods : {
    desName (value,index){
        return value.split('-')[index]
    },
    slice(){
        let time = this.mission.containers.length
        setTimeout(function(){
            let containers = this.mission.containers
            let stack = this.stack
            this.plus = this.stack.filter((item)=>{return containers.indexOf(item)<0 })
            this.minus = this.mission.containers.filter((item)=>{return stack.indexOf(item)<0})
            this.stack = []
            this.slice()
            if(this.missionStart){
                let mission = 'mission'+this.missionId
                let mix = this.plus.concat(this.minus)
                mix.forEach((item)=>{
                    $('.'+mission).find('.checkbox.'+item).checkbox('check')
                })
                let allchecked = true
                $('.'+mission).find('.checkbox').each(function(){
                    if(!$(this).checkbox('is checked')){
                            allchecked = false
                        }
                })
                this.allchecked = allchecked
            }
        }.bind(this),5000)
    },
    examine(){
        this.checkSocket = new WebSocket("ws://localhost:5000")
        this.checkSocket.onmessage = function(event){
                        let containerNumber = String(event.data)
                        if(this.stack.indexOf(containerNumber)<0){
                            this.stack.push(containerNumber)
                        }
        }.bind(this)
            this.slice()
    },
    handsetUpdate(){
            if(!this.handSocket){
                this.handSocket = new WebSocket("ws://localhost:7001")
            }
            this.handSocket.onmessage = function(event){
                let mission = 'handset'+this.missionId
                let $checkbox = $('.'+mission).find('.checkbox')
                let allverify = this.allverify
                let containerNumber = event.data
                allverify = true
                $('.'+mission).find('.checkbox.'+containerNumber).checkbox('check')
                $checkbox.each(function(){
                    if(!$(this).checkbox('is checked')){
                        allverify = false
                    }
                })
                this.allverify = allverify
            }.bind(this)
    },
    update(){
        let port = this.port + this.update_port
        let phone = this.userInfo.phone
        let task_pk = this.mission.tasksInfo[this.current].task_pk
        let data = {"phone":phone,"task_pk":task_pk}
        ajax.post(port,data).then(function(data){
            this.mission = data
            this.handsetUpdate()
        }.bind(this))
        this.socket.onmessage = null
        this.socket = null
    },
    handsetReceive(){
        let port = this.port + this.handset_port
        let task_pk = this.mission.tasksInfo[this.current].task_pk
        let data = {"task_pk":task_pk}
        ajax.post(port,data).then(function(data){
            this.mission = data
            this.current+=1
            this.missionStart=false
        }.bind(this))
    },
    start(){
        this.missionStart=true
        // let mission = 'mission'+this.missionId
        // let mix = this.plus.concat(this.minus)
        // mix.forEach((item)=>{
        //     $('.'+mission).find('.checkbox.'+item).checkbox('check')
        // })
        // this.socket.onmessage = function(event){
        //         let mission = 'mission'+this.missionId
        //         let $checkbox = $('.'+mission).find('.checkbox')
        //         let allchecked = this.allchecked
        //         let containerNumber = event.data
        //         allchecked = true
        //         $('.'+mission).find('.checkbox.'+containerNumber).checkbox('check')
        //         $checkbox.each(function(){
        //                 if(!$(this).checkbox('is checked')){
        //                     allchecked = false
        //                 }
        //             })
        //         this.allchecked = allchecked
        //         if(this.allchecked){
        //             this.socket.close()
        //         }
        // }.bind(this)
    },
    alert(){
        let mission_pk = this.mission.mission_pk
        this.alertSocket.send('lock-'+mission_pk+'-normal')
        $('.modal'+mission_pk).modal('show')
    },
    doorAlert(){
        let mission_pk = this.mission.mission_pk
        this.alertSocket.send('lock-'+mission_pk+'-normal')
        $('.dooralert').modal('show')
    },
    lockFront(){
        let devicePort = this.devicePort
        let frontSocket = new WebSocket("ws://localhost:4003")
        frontSocket.onmessage=function(event){
            let cleanData = event.data.replace("\n","")
            if(cleanData=="on"){
                this.frontDoorLocked=true
            }
        }.bind(this)
        setTimeout(function(){
            new Image().src=devicePort+"/ecmd?pin%20set%20k1%20on"
            setTimeout(function(){
                new Image().src=devicePort+"/ecmd?pin%20set%20k2%20on"
                setTimeout(function(){
                    new Image().src=devicePort+"/ecmd?pin%20set%20k1%20off"
                    setTimeout(function(){
                        new Image().src=devicePort+"/ecmd?pin%20set%20k2%20off"
                       setTimeout(function(){
                          if(!this.frontDoorLocked){
                            this.lockFront()
                          }
                       },2000)
                    },1000)
                },1000)
            },1000)
        },0)
    },
    lockBack(){
        let devicePort = this.devicePort
        let backSocket = new WebSocket("ws://localhost:4004")
        backSocket.onmessage=function(event){
            let cleanData = event.data.replace("\n","")
            if(cleanData=="on"){
                this.backDoorLocked=true
            }
        }.bind(this)
        setTimeout(function(){
            new Image().src=devicePort+"/ecmd?pin%20set%20k3%20on"
            setTimeout(function(){
                new Image().src=devicePort+"/ecmd?pin%20set%20k4%20on"
                setTimeout(function(){
                    new Image().src=devicePort+"/ecmd?pin%20set%20k3%20off"
                    setTimeout(function(){
                        new Image().src=devicePort+"/ecmd?pin%20set%20k4%20off"
                        setTimeout(function(){
                          if(!this.backDoorLocked){
                            this.lockBack()
                          }
                       },2000)
                    },1000)
                },1000)
            },1000)
        },0)
    },
    unlockFront(){
        let devicePort = this.devicePort
        let frontSocket = new WebSocket("ws://localhost:4003")
        frontSocket.onmessage=function(event){
            let cleanData = event.data.replace("\n","")
            if(cleanData=="on"){
                this.frontDoorLocked=true
            }
        }.bind(this)
        setTimeout(function(){
            new Image().src=devicePort+"/ecmd?pin%20set%20k2%20on"
            setTimeout(function(){
                new Image().src=devicePort+"/ecmd?pin%20set%20k1%20on"
                setTimeout(function(){
                    new Image().src=devicePort+"/ecmd?pin%20set%20k2%20off"
                    setTimeout(function(){
                        new Image().src=devicePort+"/ecmd?pin%20set%20k1%20off"
                        setTimeout(function(){
                          if(this.frontDoorLocked){
                            this.unlockFront()
                          }
                       },2000)
                    },500)
                },500)
            },500)
        },0)
    },
    unlockBack(){
        let devicePort = this.devicePort
        let backSocket = new WebSocket("ws://localhost:4004")
        backSocket.onmessage=function(event){
            let cleanData = event.data.replace("\n","")
            if(cleanData=="on"){
                this.backDoorLocked=true
            }
        }.bind(this)
        setTimeout(function(){
            new Image().src=devicePort+"/ecmd?pin%20set%20k4%20on"
            setTimeout(function(){
                new Image().src=devicePort+"/ecmd?pin%20set%20k3%20on"
                setTimeout(function(){
                    new Image().src=devicePort+"/ecmd?pin%20set%20k4%20off"
                    setTimeout(function(){
                        new Image().src=devicePort+"/ecmd?pin%20set%20k3%20off"
                        setTimeout(function(){
                          if(this.backDoorLocked){
                            this.unlockBack()
                          }
                       },2000)
                    },500)
                },500)
            },500)
        },0)
    },
    checkDoor(){
         let doorSocket = new WebSocket("ws://localhost:4002")
         doorSocket.onmessage=function(event){
            let cleanData = event.data.replace("\n","")
            if(cleanData=="off"){
                this.doorOpen=true
            }
            if(cleanData=='on'){
                this.doorOpen=false
            }
        }.bind(this)
    },
    danger(){
        this.lockFront();
        this.lockBack()
        this.isDanger = true
        let mission_pk = this.mission.mission_pk
        this.alertSocket.send('lock-'+mission_pk+'-danger')
    },
    strike(){
        let deviceSocket = new WebSocket("ws://localhost:4001")
        deviceSocket.onmessage=function(event){
            let cleanData = event.data.replace("\n","")
            if(cleanData=="on"&&!this.isDanger){
                console.log(this.isDanger)
                this.danger()
            }
        }.bind(this)
    }
  },
  watch:{
    allverify:function(value){
        if(value){
            this.handSocket.close()
            this.handSocket = null
            this.allverify = false
            this.handsetReceive()
        }
    },
    doorOpen:function(value){
        if(value&&!this.missionStart){
            this.doorAlert()
        }
        if(!value&&!this.missionStart){
            $('.dooralert').modal('hide')
        }
    }
},
  mounted:function(){
    $('.ui.checkbox').checkbox()
    $('.ui.accordion').accordion()
    $('.ui.modal').modal()
    $('.dooralert').modal({closable:false})
    this.examine()
    this.handsetUpdate()
    this.strike()
    this.alertSocket = new WebSocket("ws://"+this.websocket);
    this.alertSocket.onmessage = function(event){
            let message=event.data
            let action = message.split('-')[0]
            let mission_pk = message.split('-')[1]
            if(action=='unlock'&&mission_pk==this.mission.mission_pk){
                this.unlockFront()
                this.unlockBack()
        }
    }.bind(this)
    this.checkDoor()
  }
}
</script>
