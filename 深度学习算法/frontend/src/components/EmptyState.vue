<template>
  <el-empty :description="text || '暂无评估结果，请先训练并评估模型'" />
</template>

<script setup>
defineProps({ text: String })
</script>

