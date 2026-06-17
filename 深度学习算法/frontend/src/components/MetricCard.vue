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
.metric {
  position: relative;
  overflow: hidden;
  background: rgba(255, 255, 255, .94);
  border: 1px solid #dfe7f3;
  border-radius: 8px;
  padding: 18px;
  box-shadow: 0 12px 28px rgba(36, 48, 66, .08);
}

.metric::before {
  content: "";
  position: absolute;
  inset: 0 0 auto;
  height: 3px;
  background: linear-gradient(90deg, #2f80ed, #18b6c9, #43b883);
}

.label {
  color: #68758a;
  font-size: 13px;
}

.value {
  margin-top: 8px;
  font-size: 28px;
  font-weight: 900;
  color: #1264a3;
  letter-spacing: 0;
}
</style>
