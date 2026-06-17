<template>
  <div class="side-shell">
    <div v-if="!collapsed" class="brand">
      <div class="brand-mark">AI</div>
      <div>
        <div class="brand-title">CIFAR Lab</div>
        <div class="brand-subtitle">Model Console</div>
      </div>
    </div>
    <el-menu
      router
      :collapse="collapsed"
      background-color="transparent"
      text-color="#c9d3e6"
      active-text-color="#ffffff"
      class="menu"
    >
      <el-menu-item index="/"><el-icon><House /></el-icon><span>首页</span></el-menu-item>
      <el-menu-item index="/predict"><el-icon><Picture /></el-icon><span>单图识别</span></el-menu-item>
      <el-menu-item index="/batch-predict"><el-icon><UploadFilled /></el-icon><span>批量预测</span></el-menu-item>
      <el-menu-item index="/compare"><el-icon><DataAnalysis /></el-icon><span>模型对比</span></el-menu-item>
      <el-menu-item index="/dataset"><el-icon><Grid /></el-icon><span>数据集分析</span></el-menu-item>
      <el-menu-item index="/about"><el-icon><InfoFilled /></el-icon><span>项目说明</span></el-menu-item>
    </el-menu>
  </div>
</template>

<script setup>
defineProps({ collapsed: Boolean })
</script>

<style scoped>
.side-shell {
  min-height: 100vh;
  padding: 16px 10px;
  background:
    linear-gradient(180deg, rgba(24, 182, 201, .12), transparent 34%),
    #162239;
}

.brand {
  display: flex;
  align-items: center;
  gap: 12px;
  height: 64px;
  padding: 0 10px;
  margin-bottom: 8px;
  color: #fff;
}

.brand-mark {
  width: 38px;
  height: 38px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border: 1px solid rgba(122, 211, 255, .5);
  border-radius: 8px;
  color: #7ad3ff;
  font-weight: 900;
  background: rgba(255, 255, 255, .06);
}

.brand-title {
  font-weight: 900;
}

.brand-subtitle {
  margin-top: 2px;
  color: #8fa4c2;
  font-size: 12px;
}

.menu {
  min-height: calc(100vh - 88px);
  border-right: none;
}

:deep(.el-menu-item) {
  margin: 6px 0;
  border-radius: 8px;
}

:deep(.el-menu-item.is-active) {
  background: linear-gradient(90deg, #2f80ed, #18b6c9);
  box-shadow: 0 10px 26px rgba(47, 128, 237, .25);
}
</style>
