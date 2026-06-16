<template>
  <div class="metric">
    <div class="label">{{ label }}</div>
    <div class="value">{{ value ?? '暂无' }}</div>
  </div>
</template>

<script setup>
defineProps({ label: String, value: [String, Number] })
</script>

<style scoped>
.metric { background: #fff; border: 1px solid #e3e8f2; border-radius: 8px; padding: 16px; }
.label { color: #748094; font-size: 13px; }
.value { margin-top: 8px; font-size: 24px; font-weight: 700; color: #1264a3; }
</style>

