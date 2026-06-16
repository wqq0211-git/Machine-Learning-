<template>
  <div class="page">
    <div class="hero">
      <div>
        <h1>CIFAR-10 图像分类双模型对比</h1>
        <p>自定义 CNN 与 ResNet-18 在同一数据集、同一系统中的训练、评估、预测和可视化展示。</p>
        <div class="actions">
          <el-button type="primary" :icon="Picture" @click="$router.push('/predict')">开始识别</el-button>
          <el-button :icon="DataAnalysis" @click="$router.push('/compare')">查看模型对比</el-button>
        </div>
      </div>
    </div>
    <div class="grid grid-3">
      <MetricCard label="数据集样本数" :value="dataset?.total_samples" />
      <MetricCard label="类别数" :value="dataset?.classes?.length" />
      <MetricCard label="模型数量" value="2" />
    </div>
    <div class="grid grid-2">
      <div class="panel"><h2>模型概览</h2><el-table :data="models"><el-table-column prop="name" label="模型" /><el-table-column prop="available" label="可用"><template #default="{ row }"><el-tag :type="row.available ? 'success' : 'warning'">{{ row.available ? '已加载' : '未加载' }}</el-tag></template></el-table-column><el-table-column prop="parameters" label="参数量" /></el-table></div>
      <div class="panel"><h2>实验流程</h2><el-steps direction="vertical" :active="4"><el-step title="下载 CIFAR-10" /><el-step title="训练 CNN 与 ResNet-18" /><el-step title="测试集评估" /><el-step title="FastAPI 推理服务" /><el-step title="Vue 可视化展示" /></el-steps></div>
    </div>
    <div class="panel">
      <h2>当前指标</h2>
      <EmptyState v-if="!metrics?.cnn && !metrics?.resnet18" />
      <MetricsBarChart v-else :metrics="metrics" />
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { DataAnalysis, Picture } from '@element-plus/icons-vue'
import { getDataset, getMetrics, getModels } from '../api/modelApi'
import MetricCard from '../components/MetricCard.vue'
import MetricsBarChart from '../components/MetricsBarChart.vue'
import EmptyState from '../components/EmptyState.vue'

const dataset = ref(null)
const metrics = ref(null)
const models = ref([])
onMounted(async () => {
  dataset.value = await getDataset()
  metrics.value = await getMetrics()
  models.value = await getModels()
})
</script>

<style scoped>
.hero {
  min-height: 240px;
  display: flex;
  align-items: center;
  color: #fff;
  background: linear-gradient(135deg, #1264a3, #1f9d8a);
  border-radius: 8px;
  padding: 36px;
  margin-bottom: 18px;
}
.hero h1 { margin: 0 0 12px; font-size: 34px; }
.hero p { max-width: 720px; line-height: 1.8; }
</style>

