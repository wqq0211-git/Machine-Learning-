<template>
  <div class="page">
    <h2 class="section-title">模型对比</h2>

    <EmptyState v-if="!metrics?.cnn && !metrics?.resnet18" />
    <template v-else>
      <div class="panel">
        <h3>测试集评测指标</h3>
        <el-table :data="metricRows" border>
          <el-table-column prop="model" label="模型" min-width="110" />
          <el-table-column prop="accuracy" label="Accuracy" min-width="110" />
          <el-table-column prop="precision" label="Macro Precision" min-width="150" />
          <el-table-column prop="recall" label="Macro Recall" min-width="130" />
          <el-table-column prop="f1" label="Macro F1" min-width="110" />
          <el-table-column prop="auc" label="Macro AUC" min-width="120" />
          <el-table-column prop="parameters" label="参数量" min-width="130" />
          <el-table-column prop="time" label="平均单张推理时间" min-width="160" />
          <el-table-column prop="samples" label="测试样本数" min-width="120" />
        </el-table>
      </div>

      <div class="panel">
        <h3>训练信息</h3>
        <el-table :data="trainingRows" border>
          <el-table-column prop="model" label="模型" />
          <el-table-column prop="bestValAccuracy" label="最佳验证准确率" />
          <el-table-column prop="epochs" label="训练轮数" />
          <el-table-column prop="device" label="设备" />
        </el-table>
      </div>

      <div class="panel">
        <h3>结论</h3>
        <p>
          ResNet-18 的测试准确率达到 {{ percent(metrics.resnet18?.accuracy) }}，
          明显高于 CNN 的 {{ percent(metrics.cnn?.accuracy) }}；CNN 参数量更少、推理更快，
          适合轻量演示；ResNet-18 参数更多但分类性能更强。
        </p>
      </div>

      <div class="panel">
        <h3>五项核心指标对比</h3>
        <MetricsBarChart :metrics="metrics" />
      </div>

      <div class="grid grid-2">
        <div class="panel">
          <h3>训练 Loss 曲线</h3>
          <TrainingCurveChart :history="history" field="train_loss" title="Train Loss" />
        </div>
        <div class="panel">
          <h3>验证 Accuracy 曲线</h3>
          <TrainingCurveChart :history="history" field="val_accuracy" title="Validation Accuracy" />
        </div>
      </div>

      <div class="grid grid-2">
        <div class="panel">
          <h3>CNN 混淆矩阵</h3>
          <ConfusionMatrixChart :matrix="cnnMatrix" />
        </div>
        <div class="panel">
          <h3>ResNet-18 混淆矩阵</h3>
          <ConfusionMatrixChart :matrix="resnetMatrix" />
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { getConfusionMatrix, getMetrics, getModelInfo, getTrainingHistory } from '../api/modelApi'
import EmptyState from '../components/EmptyState.vue'
import MetricsBarChart from '../components/MetricsBarChart.vue'
import TrainingCurveChart from '../components/TrainingCurveChart.vue'
import ConfusionMatrixChart from '../components/ConfusionMatrixChart.vue'

const metrics = ref(null)
const modelInfo = ref({})
const history = ref({})
const cnnMatrix = ref(null)
const resnetMatrix = ref(null)

const fixed = value => value == null ? '暂无' : Number(value).toFixed(4)
const percent = value => value == null ? '暂无' : `${(Number(value) * 100).toFixed(2)}%`
const intText = value => value == null ? '暂无' : Number(value).toLocaleString()
const msText = value => value == null ? '暂无' : `${Number(value).toFixed(4)} ms`

const metricRows = computed(() => [
  toMetricRow('CNN', metrics.value?.cnn),
  toMetricRow('ResNet-18', metrics.value?.resnet18)
])

const trainingRows = computed(() => [
  toTrainingRow('CNN', modelInfo.value?.cnn),
  toTrainingRow('ResNet-18', modelInfo.value?.resnet18)
])

function toMetricRow(model, data) {
  return {
    model,
    accuracy: fixed(data?.accuracy),
    precision: fixed(data?.macro_precision),
    recall: fixed(data?.macro_recall),
    f1: fixed(data?.macro_f1),
    auc: fixed(data?.macro_auc),
    parameters: intText(data?.parameters),
    time: msText(data?.avg_inference_time_ms),
    samples: intText(data?.test_samples)
  }
}

function toTrainingRow(model, data) {
  return {
    model,
    bestValAccuracy: fixed(data?.best_val_accuracy),
    epochs: intText(data?.epochs_finished),
    device: data?.device || '暂无'
  }
}

onMounted(async () => {
  metrics.value = await getMetrics()
  modelInfo.value = await getModelInfo()
  history.value = await getTrainingHistory()
  cnnMatrix.value = await getConfusionMatrix('cnn')
  resnetMatrix.value = await getConfusionMatrix('resnet18')
})
</script>

<style scoped>
.panel + .panel,
.panel + .grid,
.grid + .panel,
.grid + .grid {
  margin-top: 16px;
}

h3 {
  margin: 0 0 14px;
  font-size: 18px;
}

p {
  line-height: 1.8;
  margin: 0;
}
</style>
