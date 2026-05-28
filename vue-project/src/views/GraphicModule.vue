<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import { RouterLink } from 'vue-router'
import { apiFetch } from '@/api/http'
import { convertColorMath, hexToRgb, type ColorConvertResult } from '@/lib/graphicsModuleColor'

type GraphicSettings = {
  module_title: string
  module_description: string
  disclaimer_text: string
}

const settings = ref<GraphicSettings | null>(null)

const pickedHex = ref('#7CFC00')
const converting = ref(false)
const result = ref<ColorConvertResult | null>(null)

const rgb = ref(hexToRgb(pickedHex.value))

const moduleDescription = computed(() => {
  const text = settings.value?.module_description?.trim()
  if (!text || text.includes('Загрузите изображение для просмотра')) {
    return 'Выберите цвет для просмотра в цветовой модели CMYK'
  }
  return text
})

function runConversion() {
  converting.value = true
  try {
    result.value = convertColorMath(pickedHex.value)
  } finally {
    converting.value = false
  }
}

watch(pickedHex, () => {
  rgb.value = hexToRgb(pickedHex.value)
  runConversion()
})

onMounted(async () => {
  try {
    settings.value = await apiFetch<GraphicSettings>('/graphic-module/settings/')
  } catch {
    settings.value = null
  }
  runConversion()
})

</script>

<template>
  <div class="graphic-module-page">
    <main class="main-content">
      <div class="container">
        <div class="gm-card">
          <header>
            <h1 class="page-title">
              {{ settings?.module_title ?? 'Графический модуль визуализации' }}
            </h1>
            <p class="page-subtitle">{{ moduleDescription }}</p>
          </header>

          <div class="gm-converter-grid">
            <section class="gm-window">
              <div class="gm-window-header">
                <h2 class="gm-window-title">Исходный цвет</h2>
                <span class="gm-badge">RGB</span>
              </div>

              <div class="gm-color-row">
                <input
                  v-model="pickedHex"
                  type="color"
                  class="gm-color-input"
                  aria-label="Выбор цвета RGB"
                />
                <div class="gm-color-swatch" :style="{ background: pickedHex }" />
              </div>

              <div class="gm-color-values">
                <p>
                  <strong>RGB:</strong>
                  R: {{ rgb.r }}, G: {{ rgb.g }}, B: {{ rgb.b }}
                </p>
                <p>
                  <strong>HEX:</strong>
                  {{ pickedHex.toUpperCase() }}
                </p>
              </div>
            </section>

            <section class="gm-window">
              <div class="gm-window-header">
                <h2 class="gm-window-title">Результат печати</h2>
                <span class="gm-badge">CMYK</span>
              </div>

              <div class="gm-color-row">
                <div
                  class="gm-color-swatch gm-color-swatch--large"
                  :style="{ background: result?.previewHex ?? '#ccc' }"
                />
              </div>

              <div v-if="result" class="gm-color-values">
                <p>
                  <strong>CMYK:</strong>
                  C: {{ result.cmykPercents.c }}%, M: {{ result.cmykPercents.m }}%,
                  Y: {{ result.cmykPercents.y }}%, K: {{ result.cmykPercents.k }}%
                </p>
                <p>
                  <strong>Превью печати:</strong>
                  R: {{ result.previewRgb.r }}, G: {{ result.previewRgb.g }}, B: {{ result.previewRgb.b }}
                </p>
                <p v-if="result.inkWarning" class="gm-ink-warning">
                  Сумма чернил превышает 240% — возможны риски при печати.
                </p>
              </div>
              <div v-else-if="converting" class="gm-color-values">Конвертация…</div>

            </section>
          </div>

          <div class="gm-maket-cta">
            <p class="page-subtitle">
              Здесь показано, как выбранный цвет будет выглядеть в печати. Чтобы загрузить целый макет
              (листовку, визитку, баннер) и сравнить оригинал с CMYK-превью на экране, откройте
              инструмент проверки макета.
            </p>
            <RouterLink to="/graphic-module/maket" class="visualization-btn">
              Попробовать загрузить макет <span class="btn-arrow">→</span>
            </RouterLink>
          </div>

          <p v-if="settings?.disclaimer_text" class="gm-disclaimer">{{ settings.disclaimer_text }}</p>
          <p v-else class="gm-disclaimer">
            Важно: это визуальная аппроксимация. Фактический результат печати может отличаться
            в зависимости от оборудования, бумаги и калибровки.
          </p>
        </div>
      </div>
    </main>
  </div>
</template>

<style scoped>
.graphic-module-page {
  min-height: 100vh;
}
</style>
