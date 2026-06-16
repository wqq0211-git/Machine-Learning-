<template>
  <el-upload drag action="#" :auto-upload="false" :limit="limit" :multiple="multiple" :on-change="onChange" :on-remove="onRemove" accept=".jpg,.jpeg,.png">
    <el-icon class="upload-icon"><UploadFilled /></el-icon>
    <div>拖拽图片到这里，或点击选择</div>
    <template #tip><div class="muted">支持 JPG、JPEG、PNG，单张不超过 5MB</div></template>
  </el-upload>
</template>

<script setup>
const props = defineProps({ multiple: Boolean, limit: { type: Number, default: 1 } })
const emit = defineEmits(['change'])
const files = []
function onChange(file, fileList) {
  emit('change', props.multiple ? fileList : file.raw)
}
function onRemove(file, fileList) {
  emit('change', props.multiple ? fileList : null)
}
</script>

<style scoped>
.upload-icon { font-size: 42px; color: #2f80ed; }
</style>

