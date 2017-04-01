<template>
<div id="watcher" class="ui segment stacked">
    <div class="ui pointing secondary menu dynamic outside">
        <a class="item active" data-tab='mission'>当前任务</a>
        <a class="item" data-tab='list'>打印任务清单</a>
        <div class="right menu">
        <a class="ui button black basic" :href='port+"/container/container"'style="margin-bottom:2px">查看货箱</a>
        </div>
    </div>
    <div class="ui tab" data-tab="mission">
      <div v-for="(task,index) in tasks" >
        <task :task="task" :port="port" :userInfo="userInfo" :taskId="index"></task>
      </div>
    </div>
    <div class="ui tab" data-tab="list">
      <div class="login ui middle aligned center aligned grid" v-if="!isLogged">
        <div class="column" style="max-width:450px">
          <h2 class="ui teal image header">
            <div class="content">
              请输入指纹
            </div>
          </h2>
          <div class="ui bottom attached tab segment" data-tab="fingerprint">
            <div class="ui visible message negative" v-if="errorCode==403">
              <p>未知错误，请联系管理员</p>
              </div>
              <div class="ui visible message negative" v-if="errorCode==400">
                <p>该指纹不属于押运人员</p>
              </div>
          </div>
        </div>
      </div>
      <div v-else>
          <div class="ui secondary menu inside">
            <a class="item" :data-tab="'mission'+index" v-for="(mission,index) in list ">任务{{index+1}}</a>
            <div class="right menu">
              <button class="ui button red" @click="isLogged=false">退出</button>
            </div>

          </div>
          <div v-for="(mission,index) in list" :data-tab="'mission'+index" class="ui tab ">
            <div :id="'area'+index">
            <h4 class="ui dividing header">任务时间：{{mission.time_start}}</h4>
            <table class="ui celled table structured small black">
                <thead>
                  <tr>
                    <th>车牌号</th>
                    <th>工号</th>
                    <th>姓名</th>
                    <th>职务</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(guarder,index) in mission.guarders">
                    <td :rowspan="mission.guarders.length+1" v-if="!index">{{mission.car.license}}</td>
                    <td>{{ guarder.workerId}}</td>
                    <td>{{ guarder.name}}</td>
                    <td>押送员</td>
                  </tr>
                  <tr v-for="(guarder,index) in mission.relivers">
                    <td :rowspan="mission.guarders.length+1" v-if="!index">{{mission.car.license}}</td>
                    <td>{{ guarder.workerId}}</td>
                    <td>{{ guarder.name}}</td>
                    <td>解款员</td>
                  </tr>
                  <tr>
                    <td>{{ mission.driver.workerId }}</td>
                    <td>{{ mission.driver.name}}</td>
                    <td>司机</td>
                  </tr>
                </tbody>
            </table>
            <table class="ui celled table structured attached">
                <thead>
                  <tr>
                    <th>网点名称</th>
                    <th>装车/出库</th>
                    <th>卸车/入库</th>
                    <th>押运车确认</th>
                    <th>网点确认</th>
                  </tr>
                </thead>
                <tbody v-for="task in mission.tasksInfo">
                  <tr></tr>
                  <tr v-for="(container,i) in task.load_containers" v-if="task.load_containers.length>=task.unload_containers.length">
                    <td :rowspan="task.load_containers.length+1" v-if="!i">{{ task.origin}}</td>
                    <td>编号{{ container }}</td>
                    <td>{{task.unload_containers[i]}}</td>
                    <td v-if="!i" :rowspan="task.load_containers.length+1"></td>
                    <td v-if="!i" :rowspan="task.load_containers.length+1"></td>
                  </tr>
                  <tr v-for="(container,j) in task.unload_containers" v-if="task.unload_containers.length>task.load_containers.length">
                    <td :rowspan="task.unload_containers.length+1" v-if="!j">{{ task.origin}}</td>
                    <td>{{task.load_containers[j]}}</td>
                    <td>编号{{ container }}</td>
                    <td v-if="!j" :rowspan="task.unload_containers.length+1"></td>
                    <td v-if="!j" :rowspan="task.unload_containers.length+1"></td>
                  </tr>
                  <tr>
                    <td>总计：{{ task.load_containers.length}}</td>
                    <td>总计：{{ task.unload_containers.length}}</td>
                  </tr>
                </tbody>
            </table>
          </div>
            <button class="ui button teal massive" type="submit" @click="print(index)" style="margin-top:20px">
              打印
            </button>
        </div>
      </div>
    </div>
</div>
</template>
<script>
// ####################看守人部分
import ajax from '../../utils/ajax.js'
import task from '../mission/task'
import '../../static/js/jquery.PrintArea.js'
export default {
  name: 'watcher',
  data () {
    return {
        mission_port:"/task/get_mission_watcher",
        list_port:"/task/get_mission_driver",
        tasks:[],
        phone:"",
        list:[],
        isLogged:false,
        errorCode:"",
        print_port:"/task/print_get_mission_driver",
        socket:null
    }
  },
  props:['userInfo','port'],
  methods : {
    getForm (){
      event.preventDefault()
      let port = this.port + this.list_port
      let info = {"phone":this.phone}
      ajax.post(port,info).then(function(data){
        this.list = data
        this.isLogged = true
      }.bind(this),function(error){
        this.errorCode = error.status
      }.bind(this)).then(function(){
        $('.inside .item').tab('change tab','mission0');
      })
    },
    print(index){
      $('#area'+index).printArea({extraCss:'static/table.css'})
    },
    print_login(){
      let port = this.port + this.print_port
      this.socket = new WebSocket("ws://localhost:6001")
      this.socket.onmessage = function(event){
        let pk = Number(event.data)
        let info = {"pk":pk}
        ajax.post(port,info).then(function(data){
          this.list = data
          this.isLogged = true
        }.bind(this),function(error){
          this.errorCode = error.status
        }.bind(this)).then(function(){
          $('.inside .item').tab('change tab','mission0');
        })
      }.bind(this)
    }
  },
  mounted:function(){
    $('.outside .item').tab('change tab','mission');
    let port = this.port + this.mission_port
    let userInfo = this.userInfo
    ajax.post(port,userInfo).then(function(data){
             this.tasks = data
        }.bind(this))
    this.print_login()
  },
  components:{
    task
  }
}
</script>
