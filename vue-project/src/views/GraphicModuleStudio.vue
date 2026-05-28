<script setup lang="ts">
import { computed, onMounted, onUnmounted, ref } from 'vue'
import { RouterLink } from 'vue-router'
import {
  GRAPHICS_MODULE_ICC_PROXY,
  checkGraphicsModuleHealth,
} from '@/lib/graphicsModuleColor'

const iframeSrc = `/graphics-module/index.html?studio=1&api=${encodeURIComponent(GRAPHICS_MODULE_ICC_PROXY)}`

const backendOnline = ref<boolean | null>(null)

const frameRef = ref<HTMLIFrameElement | null>(null)
const frameHeight = ref(520)

const statusLabel = computed(() => {
  if (backendOnline.value === null) return 'Проверка сервера…'
  if (backendOnline.value) return 'ICC-профиль активен'
  return 'Упрощённый режим'
})

const statusClass = computed(() =>
  backendOnline.value ? 'studio-status--ok' : 'studio-status--warn',
)

let resizeObserver: MutationObserver | null = null
let resizeTimer: ReturnType<typeof setTimeout> | null = null
const measureTimeouts: ReturnType<typeof setTimeout>[] = []

const SITE_THEME_CSS = `
  :root {
    --brand-orange: #ff7722;
    --brand-orange-hover: #e66611;
    --brand-green: #008000;
    --font-heading: 'Open Sans', system-ui, sans-serif;
    --font-body: 'Roboto', system-ui, sans-serif;
  }
  html, body { overflow: visible !important; height: auto !important; font-family: var(--font-body); }
  body { padding: 0 !important; background: transparent !important; color: #333; }
  body.studio-embed .color-converter-module {
    max-width: 100%;
    width: 100%;
    margin: 0;
    box-shadow: none;
    border-radius: 0;
    padding: 20px 20px 12px;
  }
  body.studio-embed .module-header { display: none !important; }
  body.studio-embed .mode-section.color-mode { display: contents; }
  body.studio-embed .converter-disclaimer { display: none; }
  body.studio-embed .window-header { border-bottom-color: var(--brand-orange) !important; }
  body.studio-embed .window-badge, body.studio-embed .window-badge.cmyk {
    background: var(--brand-orange) !important;
    border-radius: 25px;
  }
  body.studio-embed .window-title {
    font-family: var(--font-heading);
    color: #333;
    font-size: 17px;
  }
  body.studio-embed .converter-window {
    border-radius: 16px;
    border: 2px solid #e8e8e8;
    background: #fff;
  }
  body.studio-embed .clear-image-btn {
    border-radius: 25px;
    border: 2px solid var(--brand-orange);
    color: var(--brand-orange);
    font-weight: 500;
    font-family: var(--font-body);
  }
  body.studio-embed .clear-image-btn:hover {
    background: var(--brand-orange);
    color: #fff;
  }
  body.studio-embed .image-upload-label {
    border-radius: 12px;
    padding: 16px;
    font-family: var(--font-body);
  }
  body.studio-embed .image-upload-label:hover,
  body.studio-embed .image-upload-label.drag-over {
    border-color: var(--brand-orange);
    background: #fff5ec;
    color: #333;
  }
  body.studio-embed .paper-type-selector {
    border-radius: 12px;
    background: #fafafa;
  }
  body.studio-embed .paper-type-selector select {
    border-radius: 12px;
    border: 2px solid #e8e8e8;
    font-family: var(--font-body);
    padding: 10px 14px;
  }
  body.studio-embed .paper-type-selector select:focus {
    border-color: var(--brand-orange);
    outline: none;
    box-shadow: 0 0 0 3px rgba(255, 119, 34, 0.12);
  }
  body.studio-embed .paper-type-selector span { color: var(--brand-orange); font-weight: 500; }
  body.studio-embed .image-preview canvas[style*="display: block"] {
    max-width: 100%;
    height: auto !important;
    border-radius: 8px;
  }
  body.studio-embed .color-values {
    font-family: var(--font-body);
    background: #fff;
  }
  body.studio-embed .color-values strong { font-family: var(--font-heading); }
  body.studio-embed .studio-download-footer {
    display: flex;
    justify-content: center;
  }
`

function injectEmbedStyles() {
  const doc = frameRef.value?.contentDocument
  if (!doc) return

  doc.body?.classList.add('studio-embed')

  if (!doc.querySelector('link[data-site-fonts]')) {
    const fonts = doc.createElement('link')
    fonts.rel = 'stylesheet'
    fonts.href =
      'https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600;700&family=Roboto:wght@400;500;700&display=swap'
    fonts.setAttribute('data-site-fonts', '1')
    doc.head.appendChild(fonts)
  }

  if (!doc.getElementById('studio-embed-styles')) {
    const style = doc.createElement('style')
    style.id = 'studio-embed-styles'
    style.textContent = SITE_THEME_CSS
    doc.head.appendChild(style)
  }
}

function measureFrameHeight() {
  const iframe = frameRef.value
  const doc = iframe?.contentDocument
  if (!doc?.body) return

  const module = doc.getElementById('colorConverterModule') as HTMLElement | null
  if (!module) return

  const height = Math.ceil(module.getBoundingClientRect().height + 4)

  if (height >= 280 && height <= 2400) {
    frameHeight.value = height
  }
}

function scheduleMeasure() {
  if (resizeTimer) clearTimeout(resizeTimer)
  resizeTimer = setTimeout(measureFrameHeight, 80)
}

function onFrameLoad() {
  injectEmbedStyles()
  measureFrameHeight()
  scheduleMeasure()
  measureTimeouts.push(setTimeout(measureFrameHeight, 300), setTimeout(measureFrameHeight, 900))

  const doc = frameRef.value?.contentDocument
  if (!doc?.body) return

  resizeObserver?.disconnect()
  resizeObserver = new MutationObserver(scheduleMeasure)
  resizeObserver.observe(doc.body, {
    childList: true,
    subtree: true,
    attributes: true,
    characterData: true,
  })

  window.addEventListener('resize', scheduleMeasure)
}

onMounted(async () => {
  backendOnline.value = await checkGraphicsModuleHealth()
})

onUnmounted(() => {
  resizeObserver?.disconnect()
  if (resizeTimer) clearTimeout(resizeTimer)
  measureTimeouts.forEach(clearTimeout)
  window.removeEventListener('resize', scheduleMeasure)
})
</script>

<template>
  <div class="studio-page">
    <main class="main-content">
      <div class="container studio-container">
        <nav class="studio-nav">
          <RouterLink to="/graphic-module" class="page-back-link">← К превью цвета</RouterLink>
        </nav>

        <header class="studio-page-head">
          <h1 class="page-title">Проверка макета RGB → CMYK</h1>
          <p class="page-subtitle">
            Загрузите изображение, сравните исходник и превью для печати, при необходимости скачайте
            результат.
          </p>
        </header>

        <ol class="studio-steps" aria-label="Как пользоваться инструментом">
          <li class="studio-step">
            <span class="studio-step__num" aria-hidden="true">1</span>
            <span class="studio-step__text">Загрузите макет в блок «Исходный цвет»</span>
          </li>
          <li class="studio-step">
            <span class="studio-step__num" aria-hidden="true">2</span>
            <span class="studio-step__text">Сравните RGB и CMYK-превью</span>
          </li>
          <li class="studio-step">
            <span class="studio-step__num" aria-hidden="true">3</span>
            <span class="studio-step__text">Скачайте изображение для печати</span>
          </li>
        </ol>

        <div v-if="backendOnline === false" class="studio-notice" role="alert">
          <p>
            <strong>Сервер ICC не запущен.</strong>
            Конвертация идёт по упрощённой формуле. Для точного профиля выполните:
            <code>.\scripts\run-graphics-module.ps1</code>
          </p>
        </div>

        <section class="studio-workspace" aria-label="Инструмент проверки макета">
          <div class="studio-workspace__head">
            <span class="studio-workspace__title">Сравнение макета до и после печати</span>
            <span class="studio-status" :class="statusClass">{{ statusLabel }}</span>
          </div>

          <div class="studio-frame-host">
            <iframe
              ref="frameRef"
              class="studio-frame"
              :src="iframeSrc"
              title="Проверка макета CMYK"
              :style="{ height: `${frameHeight}px` }"
              scrolling="no"
              @load="onFrameLoad"
            />
          </div>
        </section>

        <div class="visualization-block studio-footer-strip">
          <span class="visualization-text">
            Нужно проверить только отдельный цвет? Вернитесь к палитре RGB → CMYK.
          </span>
          <RouterLink to="/graphic-module" class="visualization-btn">
            К превью цвета <span class="btn-arrow">→</span>
          </RouterLink>
        </div>

        <p class="gm-disclaimer">
          <strong>Важно:</strong> это визуальная аппроксимация. Фактический результат печати может
          отличаться в зависимости от оборудования, типа бумаги и калибровки. Для точного
          соответствия рекомендуем заказать тестовый оттиск.
        </p>
      </div>
    </main>
  </div>
</template>

<style scoped>
.studio-page {
  min-height: 100vh;
  overflow-x: hidden;
}

.studio-nav {
  margin-bottom: 24px;
}
</style>
