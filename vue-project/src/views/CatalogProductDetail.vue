<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { apiFetch } from '@/api/http'
import {
  getCatalogProductBySlug,
  getChildProductsOf,
  productDetailPath,
  productImageUrl,
} from '../data/catalog'
import {
  CATALOG_PRODUCT_PAGES,
  type CatalogDetailBlock,
  type CatalogProductDetailContent,
} from '../data/catalogProductDetails'

const route = useRoute()

const slug = computed(() => String(route.params.slug ?? ''))

const apiPage = ref<CatalogProductDetailContent | null>(null)

const page = computed(() => apiPage.value ?? CATALOG_PRODUCT_PAGES[slug.value] ?? null)

onMounted(async () => {
  const s = slug.value
  if (!s) return
  try {
    const data = await apiFetch<{ content: CatalogProductDetailContent }>(
      `/catalog/products/${encodeURIComponent(s)}/`,
    )
    if (data.content && Object.keys(data.content).length) {
      apiPage.value = data.content
    }
  } catch {
    apiPage.value = null
  }
})

const catalogProduct = computed(() => getCatalogProductBySlug(slug.value))

const parentProduct = computed(() => {
  const parentSlug = catalogProduct.value?.parentSlug
  if (!parentSlug) return null
  return getCatalogProductBySlug(parentSlug) ?? null
})

const childProducts = computed(() => getChildProductsOf(slug.value))

const catalogBackTo = computed(() => {
  const sec = page.value?.catalogSection
  if (sec) return { path: '/catalog', query: { section: sec } }
  return '/catalog'
})

const galleryIndexes = computed(() => {
  const n = page.value?.gallerySlotCount ?? 0
  return Array.from({ length: n }, (_, i) => i)
})

const galleryGridClass = computed(() => {
  const n = page.value?.gallerySlotCount ?? 0
  return n > 3 ? 'detail-gallery detail-gallery--many' : 'detail-gallery'
})

function isUl(b: CatalogDetailBlock): b is Extract<CatalogDetailBlock, { type: 'ul' }> {
  return b.type === 'ul'
}

function isSpec(b: CatalogDetailBlock): b is Extract<CatalogDetailBlock, { type: 'spec' }> {
  return b.type === 'spec'
}
</script>

<template>
  <div v-if="page" class="app">
    <main class="main-content">
      <div class="container detail-wrap">
        <div class="detail-top-bar">
          <nav class="detail-bc" aria-label="Навигация по сайту">
            <ol class="detail-bc-list">
              <li class="detail-bc-step">
                <router-link to="/" class="detail-bc-link">Главная</router-link>
              </li>
              <li class="detail-bc-chev" aria-hidden="true">›</li>
              <li class="detail-bc-step">
                <router-link :to="catalogBackTo" class="detail-bc-link">Каталог</router-link>
              </li>
              <template v-if="parentProduct">
                <li class="detail-bc-chev" aria-hidden="true">›</li>
                <li class="detail-bc-step">
                  <router-link
                    :to="productDetailPath(parentProduct)"
                    class="detail-bc-link"
                  >
                    {{ parentProduct.title }}
                  </router-link>
                </li>
              </template>
              <li class="detail-bc-chev" aria-hidden="true">›</li>
              <li class="detail-bc-step detail-bc-step--current" aria-current="page">
                {{ page.title }}
              </li>
            </ol>
          </nav>
        </div>

        <article class="detail-article">
          <p class="detail-kicker">{{ page.kicker }}</p>
          <h1 class="detail-title">{{ page.title }}</h1>

          <p class="detail-lead">{{ page.lead }}</p>

          <section v-if="page.specParts.length" class="detail-spec" aria-labelledby="spec-heading">
            <h2 id="spec-heading" class="visually-hidden">Характеристики</h2>
            <p class="detail-spec-label">Характеристики</p>
            <p class="detail-spec-text">
              <template v-for="(part, pi) in page.specParts" :key="pi">
                <strong>{{ part.label }}</strong>{{ part.value }}<span v-if="pi < page.specParts.length - 1"> </span>
              </template>
            </p>
          </section>

          <section
            v-if="childProducts.length"
            class="detail-subcatalog"
            aria-labelledby="subcatalog-heading"
          >
            <h2 id="subcatalog-heading" class="detail-section-title">Подразделы</h2>
            <p class="detail-subcatalog-hint">Выберите вид креативного календаря</p>
            <ul class="detail-subcatalog-grid">
              <li v-for="child in childProducts" :key="child.slug" class="detail-subcatalog-item">
                <router-link :to="productDetailPath(child)" class="detail-subcatalog-card">
                  <div class="detail-subcatalog-thumb">
                    <img
                      v-if="productImageUrl(child)"
                      :src="productImageUrl(child)"
                      :alt="child.title"
                      loading="lazy"
                    />
                    <div v-else class="detail-subcatalog-placeholder">Фото скоро</div>
                  </div>
                  <span class="detail-subcatalog-title">{{ child.title }}</span>
                  <span class="detail-subcatalog-arrow" aria-hidden="true">→</span>
                </router-link>
              </li>
            </ul>
          </section>

          <section :class="galleryGridClass" aria-label="Фотографии продукции">
            <div v-for="i in galleryIndexes" :key="i" class="detail-gallery-slot">
              <img
                v-if="page.galleryImages?.[i]"
                class="detail-gallery-img"
                :src="page.galleryImages[i]"
                :alt="`${page.title} — фото ${i + 1}`"
                loading="lazy"
              />
              <div v-else class="detail-gallery-placeholder">
                <svg class="detail-gallery-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true">
                  <rect x="3" y="5" width="18" height="14" rx="2" />
                  <circle cx="8.5" cy="10" r="1.5" />
                  <path d="M21 19l-5-5-4 4-3-3-5 5" />
                </svg>
                <span class="detail-gallery-label">Фото скоро</span>
              </div>
            </div>
          </section>

          <section class="detail-section" :aria-labelledby="'section-' + slug">
            <h2 :id="'section-' + slug" class="detail-section-title">{{ page.sectionTitle }}</h2>
            <template v-for="(block, bi) in page.blocks" :key="bi">
              <p v-if="block.type === 'p'" class="detail-body">{{ block.text }}</p>
              <p v-else-if="block.type === 'lead-strong'" class="detail-body detail-body-strong">{{ block.text }}</p>
              <h3
                v-else-if="block.type === 'subsection'"
                class="detail-subsection-title"
                :id="'subsection-' + slug + '-' + bi"
              >
                {{ block.text }}
              </h3>
              <section
                v-else-if="isSpec(block)"
                class="detail-spec detail-spec--in-section"
                :aria-label="'Характеристики: дополнительно'"
              >
                <p class="detail-spec-label">Характеристики</p>
                <p class="detail-spec-text">
                  <template v-for="(part, pi) in block.parts" :key="pi">
                    <strong>{{ part.label }}</strong>{{ part.value }}<span v-if="pi < block.parts.length - 1"> </span>
                  </template>
                </p>
              </section>
              <ul v-else-if="isUl(block)" class="detail-list">
                <li v-for="(item, li) in block.items" :key="li">{{ item }}</li>
              </ul>
              <p v-else-if="block.type === 'accent'" class="detail-body detail-body-accent">{{ block.text }}</p>
            </template>
          </section>

          <div class="detail-cta">
            <router-link to="/contacts" class="detail-order-btn">
              Заказать
              <svg class="detail-order-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M5 12h14M12 5l7 7-7 7" />
              </svg>
            </router-link>
          </div>
        </article>
      </div>
    </main>
  </div>
</template>

<style scoped>
.visually-hidden {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

.detail-wrap {
  padding-bottom: 48px;
}

.detail-top-bar {
  max-width: 900px;
  margin: 0 auto 36px;
  padding: 20px 24px;
  background: linear-gradient(165deg, #fafcfa 0%, #f4f7f4 45%, #fffaf6 100%);
  border: 1px solid rgba(0, 128, 0, 0.14);
  border-radius: 18px;
  box-shadow: 0 10px 32px rgba(0, 0, 0, 0.05);
}

.detail-bc {
  min-width: 0;
}

.detail-bc-list {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 8px 12px;
  margin: 0;
  padding: 0;
  list-style: none;
}

.detail-bc-step {
  margin: 0;
  font-family: var(--font-body);
  font-size: clamp(1rem, 2.4vw, 1.15rem);
  line-height: 1.35;
  color: #2a2a2a;
}

.detail-bc-link {
  color: #008000;
  font-weight: 700;
  text-decoration: none;
  border-bottom: 2px solid transparent;
  transition:
    color 0.2s ease,
    border-color 0.2s ease;
}

.detail-bc-link:hover {
  color: #006600;
  border-bottom-color: rgba(0, 128, 0, 0.35);
}

.detail-bc-chev {
  color: rgba(255, 119, 34, 0.85);
  font-weight: 700;
  font-size: 1.1rem;
  line-height: 1;
  user-select: none;
  padding: 0 2px;
}

.detail-bc-step--current {
  font-family: var(--font-heading);
  font-weight: 700;
  color: #1f1f1f;
  letter-spacing: -0.01em;
}

.detail-article {
  max-width: 900px;
  margin: 0 auto;
}

.detail-kicker {
  display: inline-block;
  margin: 0 0 12px;
  padding: 6px 14px;
  font-size: 0.7rem;
  font-weight: 700;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: #008000;
  background: linear-gradient(135deg, rgba(0, 128, 0, 0.1) 0%, rgba(0, 128, 0, 0.04) 100%);
  border: 1px solid rgba(0, 128, 0, 0.28);
  border-radius: 999px;
  box-shadow: 0 2px 8px rgba(0, 128, 0, 0.08);
}

.detail-title {
  margin: 0 0 20px;
  font-family: var(--font-heading);
  font-size: clamp(1.85rem, 4.5vw, 2.5rem);
  font-weight: 700;
  line-height: 1.15;
  letter-spacing: -0.02em;
  color: #008000;
}

.detail-lead {
  margin: 0 0 28px;
  font-size: 1.08rem;
  line-height: 1.65;
  color: #3a3a3a;
  white-space: pre-line;
}

.detail-subsection-title {
  margin: 24px 0 14px;
  font-family: var(--font-heading);
  font-size: clamp(1.12rem, 2.6vw, 1.35rem);
  font-weight: 700;
  line-height: 1.3;
  color: #ff7722;
  letter-spacing: -0.01em;
}

.detail-section-title + .detail-subsection-title {
  margin-top: 10px;
}

.detail-subcatalog {
  margin-bottom: 36px;
}

.detail-subcatalog-hint {
  margin: 0 0 16px;
  font-size: 0.92rem;
  color: #666;
}

.detail-subcatalog-grid {
  list-style: none;
  margin: 0;
  padding: 0;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 16px;
}

.detail-subcatalog-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 14px;
  background: #fafcfa;
  border: 1px solid rgba(0, 128, 0, 0.16);
  border-radius: 10px;
  text-decoration: none;
  color: inherit;
  transition:
    border-color 0.2s,
    box-shadow 0.2s,
    transform 0.2s;
}

.detail-subcatalog-card:hover {
  border-color: rgba(0, 128, 0, 0.45);
  box-shadow: 0 6px 20px rgba(0, 80, 0, 0.08);
  transform: translateY(-2px);
}

.detail-subcatalog-thumb {
  flex-shrink: 0;
  width: 56px;
  height: 56px;
  border-radius: 8px;
  overflow: hidden;
  background: #eee;
}

.detail-subcatalog-thumb img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.detail-subcatalog-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.65rem;
  color: #888;
  text-align: center;
  padding: 4px;
}

.detail-subcatalog-title {
  flex: 1;
  font-size: 0.95rem;
  font-weight: 600;
  color: #222;
  line-height: 1.35;
}

.detail-subcatalog-arrow {
  flex-shrink: 0;
  color: #ff7722;
  font-size: 1.1rem;
  font-weight: 700;
}

.detail-spec--in-section {
  margin: 20px 0 8px;
}

.detail-spec {
  margin: 0 0 32px;
  padding: 20px 22px 20px 20px;
  border-radius: 0 16px 16px 0;
  background: linear-gradient(90deg, rgba(255, 119, 34, 0.1) 0%, rgba(255, 255, 255, 0.95) 55%);
  border: 1px solid rgba(0, 128, 0, 0.12);
  border-left: 4px solid #ff7722;
  box-shadow: 0 6px 24px rgba(0, 0, 0, 0.05);
}

.detail-spec-label {
  display: inline-block;
  margin: 0 0 10px;
  padding: 4px 12px;
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: #fff;
  background: linear-gradient(135deg, #ff8833, #ff7722);
  border-radius: 8px;
}

.detail-spec-text {
  margin: 0;
  font-size: 0.98rem;
  line-height: 1.55;
  color: #333;
}

.detail-spec-text strong {
  color: #008000;
  font-weight: 700;
}

.detail-gallery {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 14px;
  margin: 0 0 36px;
}

.detail-gallery--many {
  grid-template-columns: repeat(auto-fill, minmax(min(100%, 200px), 1fr));
}

.detail-gallery-slot {
  border-radius: 14px;
  overflow: hidden;
  border: 1px solid rgba(0, 0, 0, 0.07);
  box-shadow: 0 8px 26px rgba(0, 0, 0, 0.06);
  aspect-ratio: 4 / 3;
  background: linear-gradient(145deg, #ecf3ec 0%, #f4f0ea 55%, #faf8f5 100%);
}

.detail-gallery-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.detail-gallery-placeholder {
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 20px;
  color: #6e8570;
  background-image: radial-gradient(circle at 1px 1px, rgba(0, 128, 0, 0.07) 1px, transparent 0);
  background-size: 18px 18px;
}

.detail-gallery-icon {
  width: 48px;
  height: 48px;
  opacity: 0.5;
}

.detail-gallery-label {
  font-size: 0.82rem;
  font-weight: 600;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: #5c6e5e;
}

.detail-section {
  margin-bottom: 36px;
}

.detail-section-title {
  margin: 0 0 16px;
  padding-bottom: 10px;
  font-family: var(--font-heading);
  font-size: clamp(1.25rem, 3vw, 1.55rem);
  font-weight: 700;
  color: #ff7722;
  border-bottom: 2px solid rgba(255, 119, 34, 0.35);
}

.detail-body {
  margin: 0 0 14px;
  font-size: 1rem;
  line-height: 1.65;
  color: #3d3d3d;
}

.detail-body:last-of-type {
  margin-bottom: 0;
}

.detail-body-strong {
  font-weight: 700;
  color: #2d2d2d;
}

.detail-body-accent {
  padding: 16px 18px;
  border-radius: 12px;
  background: linear-gradient(120deg, rgba(0, 128, 0, 0.07), rgba(255, 119, 34, 0.08));
  border-left: 3px solid #008000;
  font-weight: 600;
  color: #2f2f2f;
}

.detail-list {
  margin: 0 0 18px;
  padding: 0;
  list-style: none;
}

.detail-list li {
  position: relative;
  margin-bottom: 10px;
  padding-left: 22px;
  font-size: 1rem;
  line-height: 1.5;
  color: #3d3d3d;
}

.detail-list li::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0.55em;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: linear-gradient(135deg, #ff7722, #ff9933);
  box-shadow: 0 0 0 2px rgba(255, 119, 34, 0.25);
}

.detail-cta {
  display: flex;
  justify-content: center;
  padding-top: 8px;
}

.detail-order-btn {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 15px 40px;
  font-size: 1.05rem;
  font-weight: 700;
  color: #fff;
  text-decoration: none;
  border-radius: 999px;
  background: linear-gradient(135deg, #ff8833 0%, #ff7722 45%, #f06518 100%);
  box-shadow: 0 8px 28px rgba(255, 119, 34, 0.4);
  transition:
    transform 0.2s ease,
    box-shadow 0.2s ease,
    filter 0.2s ease;
}

.detail-order-btn:hover {
  filter: brightness(1.06);
  box-shadow: 0 10px 34px rgba(255, 119, 34, 0.48);
  transform: translateY(-2px);
}

.detail-order-arrow {
  width: 22px;
  height: 22px;
}

@media (max-width: 768px) {
  .detail-top-bar {
    padding: 18px 20px;
  }

  .detail-bc-list {
    justify-content: flex-start;
  }

  .detail-gallery,
  .detail-gallery--many {
    grid-template-columns: 1fr;
  }
}

@media (prefers-reduced-motion: reduce) {
  .detail-order-btn {
    transition: none;
  }

  .detail-order-btn:hover {
    transform: none;
  }
}
</style>
