<template>
  <div class="page">
    <h2 class="section-title">单张图像识别</h2>
    <div class="grid grid-2">
      <div class="panel">
        <ImageUploader @change="setFile" />
        <el-image v-if="preview" :src="preview" fit="contain" class="preview" />
        <el-radio-group v-model="modelName">
          <el-radio-button label="cnn">CNN</el-radio-button>
          <el-radio-button label="resnet18">ResNet-18</el-radio-button>
          <el-radio-button label="both">双模型对比</el-radio-button>
        </el-radio-group>
        <div class="actions">
          <el-button type="primary" :loading="loading" :disabled="!file" @click="submit">开始预测</el-button>
          <el-button @click="reset">重置</el-button>
        </div>
      </div>
      <div>
        <PredictionCard v-if="modelName !== 'both'" title="预测结果" :result="singleResult" />
        <div v-else class="grid">
          <PredictionCard title="CNN 结果" :result="compareResult?.cnn" />
          <PredictionCard title="ResNet-18 结果" :result="compareResult?.resnet18" />
          <div v-if="compareResult" class="panel">预测一致：{{ compareResult.same_prediction ? '是' : '否' }}，置信度差值：{{ (compareResult.confidence_gap * 100).toFixed(2) }}%</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { predictCompare, predictSingle } from '../api/modelApi'
import ImageUploader from '../components/ImageUploader.vue'
import PredictionCard from '../components/PredictionCard.vue'

const file = ref(null)
const preview = ref('')
const modelName = ref('cnn')
const loading = ref(false)
const singleResult = ref(null)
const compareResult = ref(null)
function setFile(raw) {
  if (preview.value) URL.revokeObjectURL(preview.value)
  file.value = raw
  preview.value = raw ? URL.createObjectURL(raw) : ''
  singleResult.value = null
  compareResult.value = null
}
async function submit() {
  if (!file.value) return
  loading.value = true
  try {
    if (modelName.value === 'both') compareResult.value = await predictCompare(file.value)
    else singleResult.value = await predictSingle(file.value, modelName.value)
  } finally {
    loading.value = false
  }
}
function reset() {
  setFile(null)
}
</script>

<style scoped>
.preview { width: 100%; height: 240px; margin: 16px 0; background: #f0f3f8; border-radius: 8px; }
</style>

