<template>
  <el-container class="shell">
    <el-aside :width="asideWidth" class="aside">
      <SideMenu :collapsed="collapsed" />
    </el-aside>
    <el-container class="content-shell" :style="{ marginLeft: asideWidth }">
      <el-header class="header">
        <HeaderBar v-model:collapsed="collapsed" />
      </el-header>
      <el-main>
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { computed, ref } from 'vue'
import HeaderBar from '../components/HeaderBar.vue'
import SideMenu from '../components/SideMenu.vue'

const collapsed = ref(false)
const asideWidth = computed(() => collapsed.value ? '64px' : '230px')
</script>

<style scoped>
.shell { min-height: 100vh; }
.aside {
  position: fixed;
  inset: 0 auto 0 0;
  z-index: 20;
  height: 100vh;
  overflow: hidden;
  background: #172033;
  transition: width .2s ease;
}
.content-shell {
  min-width: 0;
  min-height: 100vh;
  transition: margin-left .2s ease;
}
.header {
  position: sticky;
  top: 0;
  z-index: 10;
  display: flex;
  align-items: center;
  background: #fff;
  border-bottom: 1px solid #e3e8f2;
}
</style>
