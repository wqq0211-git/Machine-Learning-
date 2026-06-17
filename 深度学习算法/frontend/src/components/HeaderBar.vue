<template>
  <div class="bar">
    <el-button :icon="Fold" circle class="menu-button" @click="$emit('update:collapsed', !collapsed)" />
    <div class="title-block">
      <div class="title">基于 CNN 与 ResNet-18 的 CIFAR-10 图像分类对比系统</div>
      <div class="subtitle">FastAPI + PyTorch + Vue 3 · 双模型训练评估与推理展示</div>
    </div>
    <div class="status-chip">
      <span class="pulse"></span>
      服务运行中
    </div>
  </div>
</template>

<script setup>
import { Fold } from '@element-plus/icons-vue'
defineProps({ collapsed: Boolean })
defineEmits(['update:collapsed'])
</script>

<style scoped>
.bar {
  display: flex;
  gap: 14px;
  align-items: center;
  width: 100%;
}

.menu-button {
  border-color: #d9e4f2;
}

.title-block {
  min-width: 0;
}

.title {
  font-weight: 800;
  font-size: 18px;
  color: #172033;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.subtitle {
  color: #68758a;
  font-size: 12px;
  margin-top: 3px;
}

.status-chip {
  margin-left: auto;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  height: 32px;
  padding: 0 12px;
  border: 1px solid #cfe7dc;
  border-radius: 999px;
  color: #197c55;
  background: #eefbf5;
  font-size: 13px;
  font-weight: 700;
}

.pulse {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #43b883;
  box-shadow: 0 0 0 5px rgba(67, 184, 131, .16);
}
</style>
