<template><v-chart class="chart" :option="option" autoresize /></template>
<script setup>
import { computed } from 'vue'
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { HeatmapChart } from 'echarts/charts'
import { GridComponent, TooltipComponent, VisualMapComponent } from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'
use([HeatmapChart, GridComponent, TooltipComponent, VisualMapComponent, CanvasRenderer])
const props = defineProps({ matrix: Object })
const labels = computed(() => (props.matrix?.labels || []).map(item => item.chinese || item.english))
const values = computed(() => {
  const rows = props.matrix?.matrix || []
  return rows.flatMap((row, y) => row.map((value, x) => [x, y, value]))
})
const maxValue = computed(() => Math.max(1, ...values.value.map(item => item[2])))
const option = computed(() => ({
  tooltip: {},
  grid: { top: 20, left: 80, right: 20, bottom: 70 },
  xAxis: { type: 'category', data: labels.value, axisLabel: { rotate: 35 } },
  yAxis: { type: 'category', data: labels.value },
  visualMap: { min: 0, max: maxValue.value, orient: 'horizontal', left: 'center', bottom: 0 },
  series: [{ type: 'heatmap', data: values.value }]
}))
</script>

