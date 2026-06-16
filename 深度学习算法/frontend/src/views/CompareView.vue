<template>
  <div class="page">
    <h2 class="section-title">模型对比</h2>
    <EmptyState v-if="!metrics?.cnn && !metrics?.resnet18" />
    <template v-else>
      <div class="panel"><MetricsBarChart :metrics="metrics" /></div>
      <div class="grid grid-2">
        <div class="panel"><TrainingCurveChart :history="history" field="train_loss" title="训练 Loss" /></div>
        <div class="panel"><TrainingCurveChart :history="history" field="val_accuracy" title="验证 Accuracy" /></div>
      </div>
      <div class="grid grid-2">
        <div class="panel"><h3>CNN 混淆矩阵</h3><ConfusionMatrixChart :matrix="cnnMatrix" /></div>
        <div class="panel"><h3>ResNet-18 混淆矩阵</h3><ConfusionMatrixChart :matrix="resnetMatrix" /></div>
      </div>
    </template>
    <div class="panel">
      <h3>模型建议</h3>
      <p>CNN 参数量更小，适合快速课堂演示；ResNet-18 表达能力更强，适合迁移学习和更高准确率目标。正式结论应以训练后的真实评估指标为准。</p>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { getConfusionMatrix, getMetrics, getTrainingHistory } from '../api/modelApi'
import EmptyState from '../components/EmptyState.vue'
import MetricsBarChart from '../components/MetricsBarChart.vue'
import TrainingCurveChart from '../components/TrainingCurveChart.vue'
import ConfusionMatrixChart from '../components/ConfusionMatrixChart.vue'

const metrics = ref(null)
const history = ref({})
const cnnMatrix = ref(null)
const resnetMatrix = ref(null)
onMounted(async () => {
  metrics.value = await getMetrics()
  history.value = await getTrainingHistory()
  cnnMatrix.value = await getConfusionMatrix('cnn')
  resnetMatrix.value = await getConfusionMatrix('resnet18')
})
</script>

