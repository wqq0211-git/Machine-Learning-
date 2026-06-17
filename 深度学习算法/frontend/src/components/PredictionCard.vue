<template>
  <div class="panel">
    <h3>{{ title }}</h3>
    <template v-if="result">
      <p class="main">{{ result.class_chinese }} / {{ result.class_english }}</p>
      <p>置信度：{{ percent(result.confidence) }}，耗时：{{ result.inference_time_ms?.toFixed(2) }} ms</p>
      <el-tag v-for="item in result.top3" :key="item.index" class="tag">{{ item.chinese }} {{ percent(item.probability) }}</el-tag>
      <ProbabilityChart :probabilities="result.probabilities" />
    </template>
    <EmptyState v-else text="暂无预测结果" />
  </div>
</template>

<script setup>
import EmptyState from './EmptyState.vue'
import ProbabilityChart from './ProbabilityChart.vue'

defineProps({ title: String, result: Object })
const percent = value => value == null ? '暂无' : `${(value * 100).toFixed(2)}%`
</script>

<style scoped>
h3 { margin-top: 0; }
.main { font-size: 24px; font-weight: 700; color: #1264a3; }
.tag { margin: 0 8px 8px 0; }
</style>

