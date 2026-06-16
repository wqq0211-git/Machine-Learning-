<template>
  <el-container class="shell">
    <el-aside :width="collapsed ? '64px' : '230px'" class="aside">
      <SideMenu :collapsed="collapsed" />
    </el-aside>
    <el-container>
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
import { ref } from 'vue'
import HeaderBar from '../components/HeaderBar.vue'
import SideMenu from '../components/SideMenu.vue'

const collapsed = ref(false)
</script>

<style scoped>
.shell { min-height: 100vh; }
.aside { background: #172033; transition: width .2s ease; }
.header {
  display: flex;
  align-items: center;
  background: #fff;
  border-bottom: 1px solid #e3e8f2;
}
</style>

