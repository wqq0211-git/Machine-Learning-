<template>
  <el-menu router :collapse="collapsed" background-color="#172033" text-color="#c9d3e6" active-text-color="#69c0ff" class="menu">
    <el-menu-item index="/"><el-icon><House /></el-icon><span>首页</span></el-menu-item>
    <el-menu-item index="/predict"><el-icon><Picture /></el-icon><span>单图识别</span></el-menu-item>
    <el-menu-item index="/batch-predict"><el-icon><UploadFilled /></el-icon><span>批量预测</span></el-menu-item>
    <el-menu-item index="/compare"><el-icon><DataAnalysis /></el-icon><span>模型对比</span></el-menu-item>
    <el-menu-item index="/dataset"><el-icon><Grid /></el-icon><span>数据集分析</span></el-menu-item>
    <el-menu-item index="/about"><el-icon><InfoFilled /></el-icon><span>项目说明</span></el-menu-item>
  </el-menu>
</template>

<script setup>
defineProps({ collapsed: Boolean })
</script>

<style scoped>
.menu { min-height: 100vh; border-right: none; }
</style>

