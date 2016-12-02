<template>
<div clas="taskIn">
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
                                        <div class="content">{{task.parent }}-{{ task.target }}</div>
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
                        <div class="step" data-tab='abc'>
                            <i class="flag icon"></i>
                            <div class="content">
                                <div class="title">出车</div>
                                <div class="description"></div>
                            </div>
                        </div>
                        <div class="step" v-for="task in mission.tasksInfo">
                            <i class="cube icon"></i>
                            <div class="content">
                              <div class="title">{{ task.target }}</div>
                              <div class="description">{{ task.parent }}</div>
                            </div>
                        </div>
                        <div class="step" data-tab="cbd">
                            <i class="truck icon"></i>
                            <div class="content">
                                <div class="title">卸货</div>
                                <div class="description"></div>
                            </div>
                        </div>
                        <div class="step">
                            <i class="cubes icon"></i>
                            <div class="content">
                                <div class="title">入库</div>
                            </div>
                        </div>
                    </div>
                    <div class="ui attached segment">
                        <p></p>
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
  name: 'taskIn',
  data () {
    return {

    }
  },
  props:['mission'],
  methods : {
  }
}
</script>
