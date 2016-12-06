<template>
    <div id="userPanel" class="ui container">
      <div class="ui menu">
        <div class="header item">
          {{ userInfo.partment }}
        </div>
        <a class="item">
          操作员：{{ userInfo.name }}
        </a>
        <a class="item">
          工号：{{ userInfo.workerId }}
        </a>
        <div class="right menu">
          <a class="item" @click="logout" >登出</a>
        </div>
      </div>
        <Watcher :userInfo="userInfo" v-if="userInfo.profile =='watcher'" :port="port"></Watcher>
        <Banker :userInfo="userInfo" v-if="userInfo.profile =='banker'" :port="port"></Banker>
        <Guarder :userInfo="userInfo" v-if="userInfo.profile =='guarder'" :port="port"></Guarder>
        <Driver :userInfo="userInfo" v-if="userInfo.profile =='driver'" :port="port"></Driver>
    </div>
</template>
<script>
// ####################用户面板
import Watcher from './User/Watcher'
import Guarder from './User/Guarder'
import Banker from './User/Banker'
import Driver from './User/Driver'
export default {
  name: 'UserPanel',
  data () {
    return {

    }
  },
  props:['userInfo','port'],
  methods : {
    logout:function(){
      this.$emit('logout')
    }
  },
  components: {
    Watcher,
    Banker,
    Guarder,
    Driver
  },
}
</script>
