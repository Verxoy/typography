<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { apiFetch } from '@/api/http'
import Icon from '../components/Icon.vue'

type GraphicSettings = {
  banner_title: string
  banner_text: string
  module_title: string
  module_description: string
  max_upload_mb: number
  allowed_formats: string
  show_promo_banner: boolean
  disclaimer_text: string
}

const settings = ref<GraphicSettings | null>(null)

const originalImage = ref<string | null>(null)
const processedImage = ref<string | null>(null)
const isDragging = ref(false)

const handleFileUpload = (event: Event) => {
  const input = event.target as HTMLInputElement
  if (input.files && input.files[0]) {
    const reader = new FileReader()
    reader.onload = (e) => {
      originalImage.value = e.target?.result as string
      processedImage.value = e.target?.result as string
    }
    reader.readAsDataURL(input.files[0])
  }
}

const handleDrop = (event: DragEvent) => {
  event.preventDefault()
  isDragging.value = false

  if (event.dataTransfer?.files && event.dataTransfer.files[0]) {
    const reader = new FileReader()
    reader.onload = (e) => {
      originalImage.value = e.target?.result as string
      processedImage.value = e.target?.result as string
    }
    reader.readAsDataURL(event.dataTransfer.files[0])
  }
}

const handleDragOver = (event: DragEvent) => {
  event.preventDefault()
  isDragging.value = true
}

const handleDragLeave = () => {
  isDragging.value = false
}

const clearImages = () => {
  originalImage.value = null
  processedImage.value = null
}

onMounted(async () => {
  try {
    settings.value = await apiFetch<GraphicSettings>('/graphic-module/settings/')
  } catch {
    settings.value = null
  }
})
</script>

<template>
  <div class="graphic-module-page">
    <!-- Шапка (такая же как на главной) -->
    <!-- Шапка -->
    <main class="main-content">
      <div class="container">
        <!-- Баннер (такой же как на главной) -->
        <div v-if="settings?.show_promo_banner !== false" class="banner">
          <div class="banner-content">
            <h1 class="banner-title">{{ settings?.banner_title ?? 'КАЛЕНДАРИ НА 2025 ГОД!' }}</h1>
            <p class="banner-text">
              {{
                settings?.banner_text ??
                'Мы создаем и производим любые типы календарей, а если потребуется, разработаем для Вас уникальный макет.'
              }}
            </p>
          </div>
          <div class="banner-controls">
            <button class="banner-btn">←</button>
            <button class="banner-btn">→</button>
          </div>
        </div>

        <!-- Графический модуль -->
        <div class="graphic-module">
          <div class="module-header">
            <h1 class="module-title">{{ settings?.module_title ?? 'Графический модуль визуализации' }}</h1>
            <p class="module-description">
              {{
                settings?.module_description ??
                'Загрузите изображение для просмотра в цветовой модели CMYK и сравните с оригиналом'
              }}
            </p>
            <p v-if="settings?.disclaimer_text" class="module-disclaimer">{{ settings.disclaimer_text }}</p>
          </div>

          <div class="image-comparison" 
               @drop="handleDrop" 
               @dragover="handleDragOver"
               @dragleave="handleDragLeave">
            
            <!-- Левая часть - загрузка -->
            <div class="image-section">
              <div class="upload-area" :class="{ dragging: isDragging }">
                <input 
                  v-if="!originalImage"
                  type="file" 
                  accept="image/*" 
                  @change="handleFileUpload"
                  class="file-input"
                  id="file-upload"
                />
                
                <label v-if="!originalImage" for="file-upload" class="upload-label">
                  <div class="upload-icon">📁</div>
                  <p class="upload-text">Нажмите здесь, чтобы загрузить фото</p>
                  <p class="upload-hint">или перетащите файл сюда</p>
                </label>

                <img v-else :src="originalImage" alt="Original" class="uploaded-image" />
              </div>
              <div class="section-info">
                <p>Загрузите изображение для визуализации в печатной<br>цветовой модели CMYK</p>
              </div>
            </div>

            <!-- Правая часть - результат -->
            <div class="image-section">
              <div class="result-area">
                <img v-if="processedImage" :src="processedImage" alt="Processed" class="uploaded-image" />
                <div v-else class="placeholder">
                  <div class="placeholder-icon">🖼️</div>
                  <p>Результат появится здесь</p>
                </div>
              </div>
              <div class="section-info">
                <p>Результат печати CMYK. Сравните цветопередачу и<br>примите решение о согласовании макета.</p>
              </div>
            </div>
          </div>

          <!-- Кнопки управления -->
          <div v-if="originalImage" class="controls">
            <button class="btn btn-clear" @click="clearImages">
              <span>🗑️</span> Очистить
            </button>
            <button class="btn btn-download">
              <span>💾</span> Скачать результат
            </button>
          </div>

          <!-- Информация о цветовых моделях -->
          <div class="color-info">
            <div class="info-card">
              <h3>RGB</h3>
              <p>Цветовая модель для экранов. Использует аддитивное смешение цветов (красный, зеленый, синий).</p>
            </div>
            <div class="info-card">
              <h3>CMYK</h3>
              <p>Цветовая модель для печати. Использует субтрактивное смешение (голубой, пурпурный, желтый, черный).</p>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<style>
.graphic-module-page {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.main-content {
  flex: 1;
  padding: 40px 20px;
  background: #f5f5f5;
}

/* Графический модуль */
.graphic-module {
  background: white;
  border-radius: 15px;
  padding: 40px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  
}

.module-header {
  text-align: center;
  margin-bottom: 40px;
}

.module-title {
  font-size: 32px;
  color: #333;
  margin-bottom: 10px;
  font-family: var(--font-heading);
}

.module-description {
  font-size: 16px;
  color: #666;
}

/* Область сравнения изображений */
.image-comparison {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 30px;
  margin-bottom: 30px;
}

.image-section {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.upload-area,
.result-area {
  background: #e0e0e0;
  border-radius: 10px;
  min-height: 400px;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  position: relative;
  transition: all 0.3s;
}

.upload-area.dragging {
  background: #c8e6c9;
  border: 3px dashed #4caf50;
}

.file-input {
  display: none;
}

.upload-label {
  cursor: pointer;
  text-align: center;
  padding: 40px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 15px;
}

.upload-icon {
  font-size: 64px;
  opacity: 0.5;
}

.upload-text {
  font-size: 18px;
  color: #4a90e2;
  font-weight: 500;
  text-decoration: underline;
}

.upload-hint {
  font-size: 14px;
  color: #999;
}

.uploaded-image {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.placeholder {
  text-align: center;
  padding: 40px;
  color: #999;
}

.placeholder-icon {
  font-size: 64px;
  margin-bottom: 15px;
  opacity: 0.5;
}

.section-info {
  background: #f5f5f5;
  padding: 15px;
  border-radius: 8px;
  text-align: center;
}

.section-info p {
  font-size: 14px;
  color: #333;
  line-height: 1.5;
}

/* Кнопки управления */
.controls {
  display: flex;
  gap: 15px;
  justify-content: center;
  margin-bottom: 40px;
}

.btn {
  padding: 12px 25px;
  border: none;
  border-radius: 25px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s;
}

.btn-clear {
  background: #f5f5f5;
  color: #333;
}

.btn-clear:hover {
  background: #e0e0e0;
}

.btn-download {
  background: #ff7722;
  color: white;
}

.btn-download:hover {
  background: #e66611;
  transform: translateY(-2px);
}

/* Информация о цветовых моделях */
.color-info {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  padding-top: 30px;
  border-top: 2px solid #e0e0e0;
}

.info-card {
  background: #f9f9f9;
  padding: 25px;
  border-radius: 10px;
  border-left: 4px solid #ff7722;
}

.info-card h3 {
  font-size: 20px;
  color: #333;
  margin-bottom: 10px;
  font-family: var(--font-heading);
}

.info-card p {
  font-size: 14px;
  color: #666;
  line-height: 1.6;
}

/* Адаптивность */
@media (max-width: 768px) {
  .graphic-module {
    padding: 25px;
  }

  .module-title {
    font-size: 24px;
  }

  .image-comparison {
    grid-template-columns: 1fr;
    gap: 20px;
  }

  .upload-area,
  .result-area {
    min-height: 300px;
  }

  .color-info {
    grid-template-columns: 1fr;
  }

  .controls {
    flex-direction: column;
  }

  .btn {
    width: 100%;
    justify-content: center;
  }
}
</style>