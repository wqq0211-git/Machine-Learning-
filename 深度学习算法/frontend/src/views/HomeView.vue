<template>
  <div class="page">
    <div class="hero">
      <div class="hero-copy">
        <div class="eyebrow">CIFAR-10 Vision Benchmark</div>
        <h1>CIFAR-10 图像分类双模型对比</h1>
        <p>自定义 CNN 与 ResNet-18 在同一数据集、同一系统中的训练、评估、预测和可视化展示。</p>
        <div class="actions">
          <el-button type="primary" :icon="Picture" @click="$router.push('/predict')">开始识别</el-button>
          <el-button :icon="DataAnalysis" @click="$router.push('/compare')">查看模型对比</el-button>
        </div>
      </div>

      <div class="neural-panel" aria-hidden="true">
        <div class="scan-line"></div>
        <svg viewBox="0 0 280 190" class="links">
          <path d="M42 42 L132 30 L232 58" />
          <path d="M42 42 L128 98 L232 58" />
          <path d="M42 148 L128 98 L232 58" />
          <path d="M42 148 L138 160 L232 132" />
          <path d="M128 98 L232 132" />
        </svg>
        <span class="node n1"></span>
        <span class="node n2"></span>
        <span class="node n3"></span>
        <span class="node n4"></span>
        <span class="node n5"></span>
        <span class="node n6"></span>
        <div class="hero-stat stat-a">
          <strong>{{ percent(metrics?.resnet18?.accuracy) }}</strong>
          <span>ResNet-18 Accuracy</span>
        </div>
        <div class="hero-stat stat-b">
          <strong>{{ percent(metrics?.cnn?.accuracy) }}</strong>
          <span>CNN Accuracy</span>
        </div>
      </div>
    </div>

    <div class="grid grid-3">
      <MetricCard label="数据集样本数" :value="dataset?.total_samples" />
      <MetricCard label="类别数" :value="dataset?.classes?.length" />
      <MetricCard label="模型数量" value="2" />
    </div>

    <div class="grid grid-2 overview-grid">
      <div class="panel">
        <h2>模型概览</h2>
        <el-table :data="models">
          <el-table-column prop="name" label="模型" />
          <el-table-column prop="available" label="可用">
            <template #default="{ row }">
              <el-tag :type="row.available ? 'success' : 'warning'">
                {{ row.available ? '已加载' : '未加载' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="parameters" label="参数量" />
        </el-table>
      </div>

      <div class="panel">
        <h2>实验流程</h2>
        <div class="flow-list">
          <div v-for="(step, index) in flowSteps" :key="step" class="flow-item">
            <span class="flow-index">{{ index + 1 }}</span>
            <span class="flow-text">{{ step }}</span>
          </div>
        </div>
      </div>
    </div>

    <div class="panel metrics-panel">
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
const flowSteps = ['下载 CIFAR-10', '训练 CNN 与 ResNet-18', '测试集评估', 'FastAPI 推理服务', 'Vue 可视化展示']
const percent = value => value == null ? '暂无' : `${(Number(value) * 100).toFixed(2)}%`

onMounted(async () => {
  dataset.value = await getDataset()
  metrics.value = await getMetrics()
  models.value = await getModels()
})
</script>

<style scoped>
.hero {
  position: relative;
  min-height: 300px;
  display: grid;
  grid-template-columns: minmax(0, 1fr) 360px;
  gap: 28px;
  align-items: center;
  overflow: hidden;
  color: #fff;
  background:
    linear-gradient(120deg, rgba(18, 100, 163, .96), rgba(31, 157, 138, .92)),
    repeating-linear-gradient(90deg, rgba(255,255,255,.12) 0 1px, transparent 1px 28px);
  border-radius: 8px;
  padding: 40px;
  margin-bottom: 18px;
  box-shadow: 0 24px 52px rgba(18, 100, 163, .24);
}

.hero::after {
  content: "";
  position: absolute;
  inset: auto 0 0;
  height: 5px;
  background: linear-gradient(90deg, #7ad3ff, #43b883, #f2a93b);
}

.hero h1 {
  margin: 0 0 12px;
  font-size: 38px;
  line-height: 1.18;
}

.hero p {
  max-width: 720px;
  line-height: 1.8;
  font-size: 16px;
}

.eyebrow {
  display: inline-flex;
  margin-bottom: 14px;
  padding: 5px 10px;
  border: 1px solid rgba(255, 255, 255, .28);
  border-radius: 999px;
  color: #d8f7ff;
  font-size: 12px;
  font-weight: 800;
  letter-spacing: .08em;
  text-transform: uppercase;
}

.neural-panel {
  position: relative;
  height: 220px;
  border: 1px solid rgba(255, 255, 255, .24);
  border-radius: 8px;
  background:
    linear-gradient(90deg, rgba(255,255,255,.10) 1px, transparent 1px),
    linear-gradient(0deg, rgba(255,255,255,.08) 1px, transparent 1px),
    rgba(9, 29, 54, .2);
  background-size: 24px 24px;
  box-shadow: inset 0 0 48px rgba(122, 211, 255, .16);
}

.links {
  position: absolute;
  inset: 16px 36px;
  width: calc(100% - 72px);
  height: calc(100% - 32px);
  fill: none;
  stroke: rgba(201, 242, 255, .58);
  stroke-width: 2;
}

.node {
  position: absolute;
  z-index: 1;
  width: 15px;
  height: 15px;
  border-radius: 50%;
  background: #7ad3ff;
  box-shadow: 0 0 0 6px rgba(122, 211, 255, .14), 0 0 26px rgba(122, 211, 255, .8);
}

.n1 { left: 48px; top: 48px; }
.n2 { left: 48px; bottom: 48px; }
.n3 { left: 154px; top: 38px; }
.n4 { left: 150px; top: 104px; }
.n5 { right: 58px; top: 68px; }
.n6 { right: 58px; bottom: 60px; }

.scan-line {
  position: absolute;
  inset: 0 auto 0 0;
  width: 36%;
  background: linear-gradient(90deg, transparent, rgba(122, 211, 255, .18), transparent);
  animation: scan 4s ease-in-out infinite;
}

.hero-stat {
  position: absolute;
  z-index: 2;
  min-width: 148px;
  padding: 10px 12px;
  border: 1px solid rgba(255, 255, 255, .2);
  border-radius: 8px;
  background: rgba(13, 31, 55, .62);
  backdrop-filter: blur(10px);
}

.hero-stat strong {
  display: block;
  font-size: 22px;
}

.hero-stat span {
  color: #bfefff;
  font-size: 12px;
}

.stat-a { right: 18px; top: 16px; }
.stat-b { left: 18px; bottom: 16px; }

@keyframes scan {
  0%, 100% { transform: translateX(-10%); opacity: .45; }
  50% { transform: translateX(190%); opacity: .8; }
}

.overview-grid {
  align-items: stretch;
}

.overview-grid > .panel {
  min-height: 300px;
}

.flow-list {
  display: grid;
  gap: 18px;
  margin-top: 18px;
}

.flow-item {
  display: grid;
  grid-template-columns: 28px minmax(0, 1fr);
  align-items: center;
  column-gap: 12px;
}

.flow-index {
  width: 24px;
  height: 24px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border: 2px solid #409eff;
  border-radius: 50%;
  color: #409eff;
  font-weight: 700;
  line-height: 1;
}

.flow-text {
  color: #2378d8;
  line-height: 24px;
  word-break: break-word;
}

.metrics-panel {
  margin-top: 16px;
}

@media (max-width: 900px) {
  .hero {
    grid-template-columns: 1fr;
  }

  .neural-panel {
    height: 190px;
  }
}

@media (prefers-reduced-motion: reduce) {
  .scan-line {
    animation: none;
  }
}
</style>
