<template>
    <div id="userPanel" class="ui container">
      <div class="ui menu inverted teal">
        <div class="header item">
          {{ userInfo.partment }}
        </div>
        <a class="item">
          {{ defineProfile(userInfo.profile)}}：{{ userInfo.name }}
        </a>
        <a class="item">
          工号：{{ userInfo.workerId }}
        </a>
        <div class="right menu">
          <a class="item" @click="logout" ><i class="ui icon sign out"></i>登出</a>
        </div>
      </div>
        <Watcher :userInfo="userInfo" v-if="userInfo.profile =='watcher'" :port="port"></Watcher>
        <Banker :userInfo="userInfo" v-if="userInfo.profile =='banker'" :port="port"></Banker>
        <Guarder :userInfo="userInfo" v-if="userInfo.profile =='guarder'||userInfo.profile =='driver'||userInfo.profile =='reliver'" :port="port"></Guarder>
        <Keeper :userInfo="userInfo" v-if="userInfo.profile =='keeper'":port="port"></Keeper>
    </div>
</template>
<script>
// ####################用户面板
import Watcher from './User/Watcher'
import Guarder from './User/Guarder'
import Banker from './User/Banker'
import Keeper from './User/Keeper'
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
    },
    defineProfile(profile){
      let mapping = {
        "driver":"司机",
        "banker":"银行验收员",
        "guarder":"押送员",
        "watcher":"仓库管理员",
        "reliver":"解款员",
        "keeper":"枪支管理员"
      }
      return mapping[profile]
    }
  },
  components: {
    Watcher,
    Banker,
    Guarder,
    Keeper
  },
}
</script>
