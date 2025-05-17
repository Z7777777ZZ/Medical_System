<template>
  <div>
    <div class="main" style="overflow-y: hidden; ">
      <el-container >
        <el-header class="title">
          <div style="margin-top: 12px; display: inline-block;">
            <img src="./assets/aidg-icons/logo.png"
              style=" margin-right: 20px; height: 40px;vertical-align: middle;" />
            <span style="font-size: large; font-family: 'Microsoft YaHei';
                color: black; font-weight: bold;">智慧医疗系统</span>
            <span style="margin-left: 40px; color:rgba(0, 0, 0, 0.2)">浙江大学软件工程课程项目</span>
          </div>
        </el-header>
        <el-container style="width: 100%; ">
          <el-aside class="aside" style="display: flex;">
            <el-menu active-text-color="#ffd04b" background-color="#0270c1" default-active="1" text-color="#fff"
              style="height:100%; width: 100%;" :router="true">
              <el-menu-item index="ai-diagnosis">
                <el-icon>
                  <Service />
                </el-icon>
                <span>智慧问诊</span>
              </el-menu-item>
              <el-menu-item index="doctor-search">
                <el-icon>
                  <Search />
                </el-icon>
                <span>医生查找</span>
              </el-menu-item>
              <!-- <el-menu-item index="borrow">
                <el-icon>
                  <Tickets />
                </el-icon>
                <span>借书记录查询</span>
              </el-menu-item> -->

            </el-menu>
          </el-aside>

          <el-main style="height: 100%; width: 100%; ">
            <el-scrollbar height="100%">
              <RouterView class="content" style="height: 90vh; max-height: 100%; background-color: white; color: black;" />
            </el-scrollbar>

          </el-main>
        </el-container>
      </el-container>
    </div>
  </div>
  <!-- <img alt="Vue logo" src="./assets/logo.png">
  <HelloWorld msg="Welcome to Your Vue.js App"/> -->
</template>

<script>
// import HelloWorld from './components/HelloWorld.vue'
import { RouterView } from 'vue-router'

export default {
  name: 'App',
  components: {
    // HelloWorld
    RouterView,
  }
}
</script>

<style scoped>
/* 加上scoped，否则样式会很奇怪 */
#app {
  /* font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale; */
  /* text-align: center;
  color: #2c3e50;
  margin-top: 60px; */
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  background-color: #dcdcdc;
  width: 100vw;
  height: 100vh;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.main {
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  width: 100%;
  min-height: 100%;
  height: auto;
  background-color: #dcdcdc;

}

.title {
  background-color: #ffffff;
  height: 60px;
}

.aside {
  min-height: calc(100vh - 60px);
  width: 180px;
  background-color: red;
}
</style>
