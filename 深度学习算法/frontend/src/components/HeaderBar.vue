<template>
  <div class="bar">
    <el-button :icon="Fold" circle @click="$emit('update:collapsed', !collapsed)" />
    <div>
      <div class="title">基于 CNN 与 ResNet-18 的 CIFAR-10 图像分类对比系统</div>
      <div class="subtitle">FastAPI + PyTorch + Vue 3</div>
    </div>
  </div>
</template>

<script setup>
import { Fold } from '@element-plus/icons-vue'
defineProps({ collapsed: Boolean })
defineEmits(['update:collapsed'])
</script>

<style scoped>
.bar { display: flex; gap: 14px; align-items: center; width: 100%; }
.title { font-weight: 700; font-size: 18px; }
.subtitle { color: #748094; font-size: 12px; margin-top: 2px; }
</style>

