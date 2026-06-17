<template>
  <div class="page">
    <h2 class="section-title">批量预测</h2>
    <div class="panel">
      <ImageUploader ref="uploaderRef" multiple directory :limit="200" @change="files = $event" />
      <div class="actions">
        <el-radio-group v-model="modelName">
          <el-radio-button label="cnn">CNN</el-radio-button>
          <el-radio-button label="resnet18">ResNet-18</el-radio-button>
          <el-radio-button label="both">双模型</el-radio-button>
        </el-radio-group>
        <el-button type="primary" :loading="loading" :disabled="!files.length" @click="submit">开始批量预测</el-button>
        <el-button @click="clearAll">全部清空</el-button>
        <el-button :disabled="!rows.length" @click="exportCsv">导出 CSV</el-button>
        <el-checkbox v-model="onlyDiff">只看不一致</el-checkbox>
      </div>
    </div>

    <div class="panel">
      <el-table :data="filteredRows" @sort-change="sortRows">
        <el-table-column prop="index" label="序号" width="80" />
        <el-table-column prop="filename" label="文件名" />
        <el-table-column label="CNN 类别">
          <template #default="{ row }">{{ row.results?.cnn?.class_chinese || '-' }}</template>
        </el-table-column>
        <el-table-column label="CNN 置信度" sortable="custom">
          <template #default="{ row }">{{ percent(row.results?.cnn?.confidence) }}</template>
        </el-table-column>
        <el-table-column label="ResNet 类别">
          <template #default="{ row }">{{ row.results?.resnet18?.class_chinese || '-' }}</template>
        </el-table-column>
        <el-table-column label="ResNet 置信度">
          <template #default="{ row }">{{ percent(row.results?.resnet18?.confidence) }}</template>
        </el-table-column>
        <el-table-column label="一致">
          <template #default="{ row }">{{ row.same_prediction == null ? '-' : (row.same_prediction ? '是' : '否') }}</template>
        </el-table-column>
        <el-table-column prop="error" label="错误信息" />
      </el-table>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { predictBatch } from '../api/modelApi'
import ImageUploader from '../components/ImageUploader.vue'

const uploaderRef = ref(null)
const files = ref([])
const modelName = ref('both')
const loading = ref(false)
const rows = ref([])
const onlyDiff = ref(false)
const percent = value => value == null ? '-' : `${(value * 100).toFixed(2)}%`
const filteredRows = computed(() => onlyDiff.value ? rows.value.filter(row => row.same_prediction === false) : rows.value)

async function submit() {
  loading.value = true
  try {
    const result = await predictBatch(files.value, modelName.value)
    rows.value = result.items || []
  } finally {
    loading.value = false
  }
}

function clearAll() {
  uploaderRef.value?.clear()
  files.value = []
  rows.value = []
  onlyDiff.value = false
}

function sortRows() {
  rows.value = [...rows.value].sort((a, b) => (b.results?.cnn?.confidence || 0) - (a.results?.cnn?.confidence || 0))
}

function exportCsv() {
  const head = 'index,filename,cnn_class,cnn_confidence,resnet18_class,resnet18_confidence,same,error\n'
  const body = rows.value.map(row => [
    row.index,
    row.filename,
    row.results?.cnn?.class_chinese || '',
    row.results?.cnn?.confidence || '',
    row.results?.resnet18?.class_chinese || '',
    row.results?.resnet18?.confidence || '',
    row.same_prediction ?? '',
    row.error || ''
  ].join(',')).join('\n')
  const link = document.createElement('a')
  link.href = URL.createObjectURL(new Blob([head + body], { type: 'text/csv;charset=utf-8' }))
  link.download = 'batch_predict.csv'
  link.click()
}
</script>
