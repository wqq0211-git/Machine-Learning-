<template><v-chart class="chart" :option="option" autoresize /></template>
<script setup>
import { computed } from 'vue'
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { LineChart } from 'echarts/charts'
import { GridComponent, TooltipComponent, LegendComponent } from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'
use([LineChart, GridComponent, TooltipComponent, LegendComponent, CanvasRenderer])
const props = defineProps({ history: Object, field: String, title: String })
const option = computed(() => ({
  title: { text: props.title, left: 'center', textStyle: { fontSize: 14 } },
  tooltip: { trigger: 'axis' }, legend: { top: 24 },
  grid: { top: 70, left: 44, right: 20, bottom: 36 },
  xAxis: { type: 'category', data: (props.history?.cnn || props.history?.resnet18 || []).map(row => row.epoch) },
  yAxis: { type: 'value' },
  series: ['cnn', 'resnet18'].map(model => ({ name: model, type: 'line', data: (props.history?.[model] || []).map(row => row[props.field]) }))
}))
</script>

