import request from './request'

export const getHealth = () => request.get('/health')
export const getModels = () => request.get('/models')
export const getModelInfo = () => request.get('/model-info')
export const getMetrics = () => request.get('/metrics')
export const getTrainingHistory = () => request.get('/training-history')
export const getDataset = () => request.get('/dataset')
export const getConfusionMatrix = model => request.get(`/confusion-matrix/${model}`)
export const getClassMetrics = model => request.get(`/class-metrics/${model}`)

export function predictSingle(file, modelName) {
  const form = new FormData()
  form.append('file', file)
  form.append('model_name', modelName)
  return request.post('/predict', form)
}

export function predictCompare(file) {
  const form = new FormData()
  form.append('file', file)
  return request.post('/predict/compare', form)
}

export function predictBatch(files, modelName) {
  const form = new FormData()
  files.forEach(file => form.append('files', file.raw || file))
  form.append('model_name', modelName)
  return request.post('/predict/batch', form)
}
