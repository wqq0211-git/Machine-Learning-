<template><v-chart class="chart" :option="option" autoresize /></template>
<script setup>
import { computed } from 'vue'
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { BarChart } from 'echarts/charts'
import { GridComponent, TooltipComponent, LegendComponent } from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'
use([BarChart, GridComponent, TooltipComponent, LegendComponent, CanvasRenderer])
const props = defineProps({ metrics: Object })
const names = ['accuracy', 'macro_precision', 'macro_recall', 'macro_f1', 'macro_auc']
const option = computed(() => ({
  tooltip: {}, legend: {},
  xAxis: { type: 'category', data: names },
  yAxis: { type: 'value', max: 1 },
  series: ['cnn', 'resnet18'].map(model => ({ name: model, type: 'bar', data: names.map(name => props.metrics?.[model]?.[name] ?? 0) }))
}))
</script>

