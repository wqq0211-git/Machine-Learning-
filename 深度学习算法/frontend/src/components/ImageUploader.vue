<template>
  <div class="uploader" @drop.prevent.stop="handleDrop" @dragover.prevent>
    <el-upload
      ref="uploadRef"
      drag
      action="#"
      :auto-upload="false"
      :limit="limit"
      :multiple="multiple"
      :show-file-list="false"
      :on-change="onChange"
      :on-remove="onRemove"
      accept=".jpg,.jpeg,.png"
    >
      <el-icon class="upload-icon"><UploadFilled /></el-icon>
      <div>拖拽图片或文件夹到这里，或点击选择图片</div>
      <template #tip>
        <div class="muted">支持 JPG、JPEG、PNG，单张不超过 5MB</div>
      </template>
    </el-upload>

    <div v-if="directory" class="folder-row">
      <el-button type="primary" plain @click="openFolderPicker">选择文件夹</el-button>
      <span class="muted">已选择 {{ selectedFiles.length }} 张图片</span>
      <input
        ref="folderInputRef"
        class="folder-input"
        type="file"
        multiple
        webkitdirectory
        directory
        accept=".jpg,.jpeg,.png"
        @change="onFolderChange"
      />
    </div>

    <div v-if="selectedFiles.length" class="selected-list">
      <div v-for="file in previewFiles" :key="fileKey(file)" class="selected-file">
        {{ displayName(file) }}
      </div>
      <div v-if="selectedFiles.length > previewFiles.length" class="selected-more">
        还有 {{ selectedFiles.length - previewFiles.length }} 张图片
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'

const props = defineProps({
  multiple: Boolean,
  directory: Boolean,
  limit: { type: Number, default: 1 }
})
const emit = defineEmits(['change'])
const uploadRef = ref(null)
const folderInputRef = ref(null)
const selectedFiles = ref([])
const previewFiles = computed(() => selectedFiles.value.slice(0, 16))

function isImageFile(file) {
  return /\.(jpe?g|png)$/i.test(file.name || '')
}

function normalizeFile(uploadFile) {
  return uploadFile?.raw || uploadFile
}

function emitFiles(files) {
  const normalized = files.map(normalizeFile).filter(Boolean).filter(isImageFile).slice(0, props.limit)
  selectedFiles.value = normalized
  emit('change', props.multiple ? normalized : (normalized[0] || null))
}

function onChange(file, fileList) {
  emitFiles(props.multiple ? fileList : [file])
}

function onRemove(file, fileList) {
  emitFiles(props.multiple ? fileList : [])
}

function openFolderPicker() {
  folderInputRef.value?.click()
}

function onFolderChange(event) {
  const files = Array.from(event.target.files || [])
  uploadRef.value?.clearFiles()
  emitFiles(files)
  event.target.value = ''
}

async function handleDrop(event) {
  if (!props.directory) return
  const items = Array.from(event.dataTransfer?.items || [])
  const entries = items.map(item => item.webkitGetAsEntry?.()).filter(Boolean)
  if (!entries.length) {
    emitFiles(Array.from(event.dataTransfer?.files || []))
    return
  }
  const nestedFiles = await Promise.all(entries.map(readEntry))
  uploadRef.value?.clearFiles()
  emitFiles(nestedFiles.flat())
}

function readEntry(entry) {
  if (entry.isFile) {
    return new Promise(resolve => {
      entry.file(file => resolve([file]), () => resolve([]))
    })
  }
  if (entry.isDirectory) {
    return readDirectory(entry)
  }
  return Promise.resolve([])
}

async function readDirectory(directoryEntry) {
  const reader = directoryEntry.createReader()
  const entries = []
  while (true) {
    const batch = await new Promise(resolve => reader.readEntries(resolve, () => resolve([])))
    if (!batch.length) break
    entries.push(...batch)
  }
  const files = await Promise.all(entries.map(readEntry))
  return files.flat()
}

function fileKey(file) {
  return `${file.webkitRelativePath || file.name}-${file.size}-${file.lastModified}`
}

function displayName(file) {
  return file.webkitRelativePath || file.name
}

function clear() {
  uploadRef.value?.clearFiles()
  selectedFiles.value = []
  emit('change', props.multiple ? [] : null)
}

defineExpose({ clear })
</script>

<style scoped>
.upload-icon {
  font-size: 42px;
  color: #2f80ed;
}

.folder-row {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-top: 12px;
}

.folder-input {
  display: none;
}

.selected-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 6px 12px;
  max-height: 150px;
  overflow: auto;
  margin-top: 12px;
  padding: 10px;
  border: 1px solid #dfe7f3;
  border-radius: 8px;
  background: #f8fbff;
}

.selected-file,
.selected-more {
  color: #5f6f86;
  font-size: 13px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.selected-more {
  font-weight: 700;
  color: #2f80ed;
}
</style>
