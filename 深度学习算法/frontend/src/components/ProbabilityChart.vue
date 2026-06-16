<template>
  <v-chart class="chart" :option="option" autoresize />
</template>

<script setup>
import { computed } from 'vue'
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { BarChart } from 'echarts/charts'
import { GridComponent, TooltipComponent } from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'

use([BarChart, GridComponent, TooltipComponent, CanvasRenderer])
const props = defineProps({ probabilities: { type: Array, default: () => [] } })
const option = computed(() => ({
  tooltip: {},
  grid: { left: 42, right: 20, top: 20, bottom: 70 },
  xAxis: { type: 'category', data: props.probabilities.map(item => item.chinese || item.english), axisLabel: { rotate: 35 } },
  yAxis: { type: 'value', max: 1 },
  series: [{ type: 'bar', data: props.probabilities.map(item => item.probability), itemStyle: { color: '#2f80ed' } }]
}))
</script>

