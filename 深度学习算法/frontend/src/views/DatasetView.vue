<template>
  <div class="page">
    <h2 class="section-title">数据集分析</h2>
    <div class="grid grid-3">
      <MetricCard label="总样本数" :value="dataset?.total_samples" />
      <MetricCard label="训练集" :value="dataset?.train_samples" />
      <MetricCard label="测试集" :value="dataset?.test_samples" />
    </div>
    <div class="grid grid-2">
      <div class="panel"><h3>CIFAR-10 类别</h3><el-table :data="dataset?.classes || []"><el-table-column prop="index" label="#" width="60" /><el-table-column prop="english" label="英文" /><el-table-column prop="chinese" label="中文" /></el-table></div>
      <div class="panel"><h3>预处理说明</h3><p>CNN 使用 32x32 输入、随机裁剪、水平翻转和 CIFAR-10 均值方差归一化。</p><p>ResNet-18 使用 224x224 输入、轻量数据增强和 ImageNet 均值方差归一化。</p></div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { getDataset } from '../api/modelApi'
import MetricCard from '../components/MetricCard.vue'
const dataset = ref(null)
onMounted(async () => { dataset.value = await getDataset() })
</script>

