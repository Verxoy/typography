<script setup lang="ts">
import { nextTick, ref } from 'vue'
import {
  CATALOG_PRODUCTS,
  productDetailPath,
  productImageUrl,
  sectionProductCount,
  type CatalogProduct,
} from '../data/catalog'
import { useCatalogFilters } from '../composables/useCatalogFilters'

const {
  CATALOG_SECTIONS,
  activeSectionTitle,
  pageTitle,
  searchQuery,
  WHOLE_CATALOG_TITLE,
  isGlobalSearch,
  isSearchActive,
  filteredProducts,
  catalogGridKey,
  resultsCount,
  selectSection,
  startGlobalSearch,
  exitGlobalSearch,
} = useCatalogFilters()

const searchInputRef = ref<HTMLInputElement | null>(null)

function onSearchInput(event: Event) {
  searchQuery.value = (event.target as HTMLInputElement).value
}

async function onClearSearch(event?: Event) {
  event?.preventDefault()
  event?.stopPropagation()
  searchQuery.value = ''
  await nextTick()
  searchInputRef.value?.focus()
}

function sectionCount(sectionId: (typeof CATALOG_SECTIONS)[number]['id']) {
  return sectionProductCount(sectionId)
}

function showSectionOnCard(_product: CatalogProduct) {
  return isGlobalSearch.value
}
</script>

<template>
  <div class="app">
    <main class="main-content">
      <div class="container">
        <header class="catalog-page-header">
          <h1 class="page-title">{{ pageTitle }}</h1>
          <p v-if="isSearchActive" class="catalog-results-meta">
            Найдено: {{ resultsCount }} · по всем разделам
          </p>
        </header>

        <div class="catalog-layout">
          <aside class="catalog-sidebar" aria-label="Разделы каталога">
            <p class="sidebar-heading">Разделы</p>
            <div class="sidebar-menu">
              <button
                type="button"
                class="sidebar-item"
                :class="{ active: isGlobalSearch }"
                :aria-current="isGlobalSearch ? 'true' : undefined"
                @click="startGlobalSearch"
              >
                <span class="sidebar-item-label">{{ WHOLE_CATALOG_TITLE }}</span>
                <span class="sidebar-item-count">{{ CATALOG_PRODUCTS.length }}</span>
              </button>
              <button
                v-for="section in CATALOG_SECTIONS"
                :key="section.id"
                type="button"
                class="sidebar-item"
                :class="{ active: !isGlobalSearch && activeSectionTitle === section.title }"
                :aria-current="!isGlobalSearch && activeSectionTitle === section.title ? 'true' : undefined"
                @click="selectSection(section.title)"
              >
                <span class="sidebar-item-label">{{ section.title }}</span>
                <span class="sidebar-item-count">{{ sectionCount(section.id) }}</span>
              </button>
            </div>
          </aside>

          <div class="catalog-main">
            <div v-if="isGlobalSearch" class="catalog-toolbar catalog-toolbar--search-only" role="search">
              <label class="catalog-search catalog-search--full">
                <span class="visually-hidden">Поиск по названию продукции</span>
                <svg class="catalog-search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">
                  <circle cx="11" cy="11" r="7" />
                  <path d="M20 20l-3-3" />
                </svg>
                <input
                  ref="searchInputRef"
                  :value="searchQuery"
                  type="text"
                  class="catalog-search-input"
                  placeholder="..."
                  autocomplete="off"
                  autocorrect="off"
                  autocapitalize="off"
                  spellcheck="false"
                  inputmode="search"
                  enterkeyhint="search"
                  @input="onSearchInput"
                />
                <button
                  v-show="searchQuery.length > 0"
                  type="button"
                  class="catalog-search-clear"
                  aria-label="Очистить поиск"
                  @mousedown.prevent="onClearSearch"
                >
                  ×
                </button>
              </label>

              <button type="button" class="catalog-reset-btn" @click="exitGlobalSearch">
                К разделам каталога
              </button>
            </div>

            <div v-else class="catalog-section-actions">
              <button type="button" class="catalog-global-search-btn" @click="startGlobalSearch">
                Поиск по всему каталогу
              </button>
            </div>

            <div v-if="filteredProducts.length" :key="catalogGridKey" class="product-grid">
              <router-link
                v-for="product in filteredProducts"
                :key="product.id"
                :to="productDetailPath(product)"
                class="product-card"
              >
                <span class="product-card-accent" aria-hidden="true" />
                <div class="product-thumb">
                  <img
                    v-if="productImageUrl(product)"
                    class="product-thumb-img"
                    :src="productImageUrl(product)"
                    :alt="product.title"
                    loading="lazy"
                  />
                  <div v-else class="product-thumb-placeholder">
                    <svg class="product-thumb-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true">
                      <rect x="3" y="5" width="18" height="14" rx="2" />
                      <circle cx="8.5" cy="10" r="1.5" />
                      <path d="M21 19l-5-5-4 4-3-3-5 5" />
                    </svg>
                    <span class="product-thumb-label">Фото скоро</span>
                  </div>
                </div>
                <div class="product-card-body">
                  <div class="product-card-text-wrap">
                    <span v-if="showSectionOnCard(product)" class="product-card-section">{{ product.sectionTitle }}</span>
                    <span class="product-card-text">{{ product.title }}</span>
                  </div>
                  <span class="product-card-arrow" aria-hidden="true">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M5 12h14M12 5l7 7-7 7" />
                    </svg>
                  </span>
                </div>
              </router-link>
            </div>
            <p v-else class="catalog-placeholder">
              <template v-if="isGlobalSearch && isSearchActive">
                По вашему запросу ничего не найдено. Попробуйте другое название или
                <button type="button" class="inline-link-btn" @click="onClearSearch">очистить поле</button>.
              </template>
              <template v-else>
                Список позиций для этого раздела скоро появится. По вопросам о продукции можно написать через
                <router-link to="/contacts" class="inline-link">контакты</router-link>.
              </template>
            </p>

            <div class="order-button-wrapper">
              <router-link to="/contacts" class="order-button">
                Заказать
                <svg class="arrow-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M5 12h14M12 5l7 7-7 7" />
                </svg>
              </router-link>
            </div>
          </div>
        </div>

        <section class="catalog-bottom-panel" aria-labelledby="catalog-bottom-heading">
          <div class="bottom-panel-inner">
            <div class="bottom-panel-copy">
              <h2 id="catalog-bottom-heading" class="bottom-panel-title">Примеры работ</h2>
              <p class="bottom-panel-text">
                Иллюстрации по каждой позиции появятся здесь после загрузки фотографий. Пока можно запросить образцы,
                тираж и сроки у менеджера или посмотреть возможности печати в разделе «Технологии».
              </p>
            </div>
            <div class="bottom-panel-actions">
              <router-link to="/contacts" class="bottom-panel-link primary">Контакты и заявка</router-link>
              <router-link to="/technologies" class="bottom-panel-link">Технологии</router-link>
              <router-link to="/graphic-module" class="bottom-panel-link">Графический модуль</router-link>
            </div>
          </div>
        </section>
      </div>
    </main>
  </div>
</template>

<style scoped>
/* Палитра в духе сайта: зелёный + оранжевый, нейтральные фоны */
.catalog-page-header {
  text-align: center;
  margin-bottom: 28px;
  max-width: 720px;
  margin-left: auto;
  margin-right: auto;
}

.page-title {
  font-size: clamp(1.75rem, 4vw, 2.25rem);
  color: #008000;
  margin: 0;
  font-family: var(--font-heading);
  font-weight: 700;
  letter-spacing: -0.02em;
  line-height: 1.2;
}

.catalog-results-meta {
  margin: 10px 0 0;
  font-size: 0.95rem;
  color: #555;
}

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

.catalog-toolbar {
  display: flex;
  flex-wrap: wrap;
  align-items: flex-end;
  gap: 12px 16px;
  margin-bottom: 22px;
  padding-bottom: 18px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.08);
}

.catalog-toolbar--search-only {
  align-items: center;
}

.catalog-search--full {
  flex: 1 1 100%;
  max-width: 100%;
}

.catalog-search {
  position: relative;
  flex: 1 1 220px;
  min-width: min(100%, 200px);
  display: flex;
  align-items: center;
}

.catalog-section-actions {
  margin-bottom: 22px;
}

.catalog-global-search-btn {
  display: inline-flex;
  align-items: center;
  padding: 11px 20px;
  border: 1px solid rgba(0, 128, 0, 0.35);
  border-radius: 12px;
  background: rgba(0, 128, 0, 0.06);
  color: #008000;
  font-size: 0.92rem;
  font-weight: 600;
  font-family: inherit;
  cursor: pointer;
  transition:
    background 0.2s ease,
    border-color 0.2s ease,
    box-shadow 0.2s ease;
}

.catalog-global-search-btn:hover {
  background: rgba(0, 128, 0, 0.12);
  border-color: #008000;
  box-shadow: 0 4px 14px rgba(0, 128, 0, 0.12);
}

.catalog-search-icon {
  position: absolute;
  left: 14px;
  width: 18px;
  height: 18px;
  color: #6e8570;
  pointer-events: none;
}

.catalog-search-input {
  width: 100%;
  padding: 11px 40px 11px 42px;
  border: 1px solid rgba(0, 128, 0, 0.2);
  border-radius: 12px;
  font-size: 0.95rem;
  font-family: inherit;
  background: #fff;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.catalog-search-input:focus {
  outline: none;
  border-color: #008000;
  box-shadow: 0 0 0 3px rgba(0, 128, 0, 0.12);
}

.catalog-search-clear {
  position: absolute;
  right: 8px;
  width: 28px;
  height: 28px;
  border: none;
  border-radius: 8px;
  background: transparent;
  color: #666;
  font-size: 1.25rem;
  line-height: 1;
  cursor: pointer;
}

.catalog-search-clear:hover {
  background: rgba(0, 0, 0, 0.06);
  color: #333;
}

.catalog-sort {
  display: flex;
  flex-direction: column;
  gap: 6px;
  flex: 0 1 auto;
}

.catalog-sort-label {
  font-size: 0.72rem;
  font-weight: 600;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: #6a6a6a;
}

.catalog-sort-select {
  padding: 10px 36px 10px 12px;
  border: 1px solid rgba(0, 0, 0, 0.12);
  border-radius: 12px;
  font-size: 0.9rem;
  font-family: inherit;
  background: #fff;
  cursor: pointer;
  min-width: 200px;
}

.catalog-reset-btn {
  padding: 9px 14px;
  border: 1px dashed rgba(255, 119, 34, 0.5);
  border-radius: 10px;
  background: rgba(255, 119, 34, 0.08);
  color: #c45a10;
  font-size: 0.88rem;
  font-weight: 600;
  font-family: inherit;
  cursor: pointer;
  transition: background 0.2s ease;
}

.catalog-reset-btn:hover {
  background: rgba(255, 119, 34, 0.15);
}

.sidebar-item-label {
  flex: 1;
  min-width: 0;
}

.sidebar-item-count {
  flex-shrink: 0;
  min-width: 1.5rem;
  padding: 2px 7px;
  border-radius: 999px;
  background: rgba(0, 128, 0, 0.1);
  color: #008000;
  font-size: 0.72rem;
  font-weight: 700;
  text-align: center;
  line-height: 1.3;
}

.sidebar-item.active .sidebar-item-count {
  background: rgba(255, 255, 255, 0.25);
  color: #fff;
}

.product-card-text-wrap {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.product-card-section {
  font-size: 0.72rem;
  font-weight: 600;
  color: #008000;
  line-height: 1.3;
}

.inline-link-btn {
  padding: 0;
  border: none;
  background: none;
  color: #008000;
  text-decoration: underline;
  text-underline-offset: 3px;
  font: inherit;
  cursor: pointer;
}

.inline-link-btn:hover {
  color: #006600;
}

.catalog-layout {
  display: grid;
  grid-template-columns: minmax(220px, 280px) 1fr;
  gap: clamp(20px, 3vw, 32px);
  align-items: start;
  margin-bottom: 20px;
}

.catalog-sidebar {
  position: sticky;
  top: 16px;
  background: linear-gradient(165deg, #fafafa 0%, #f0f4f0 100%);
  border-radius: 20px;
  padding: 22px 18px;
  border: 1px solid rgba(0, 128, 0, 0.12);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.06);
}

.sidebar-heading {
  margin: 0 0 14px;
  font-size: 0.75rem;
  font-weight: 600;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #008000;
  text-align: center;
}

.sidebar-menu {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.sidebar-item {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 10px;
  width: 100%;
  padding: 11px 14px;
  background: #fff;
  border: 1px solid rgba(0, 0, 0, 0.06);
  border-radius: 14px;
  color: #333;
  font-size: 13px;
  line-height: 1.35;
  text-align: left;
  transition:
    background 0.2s ease,
    border-color 0.2s ease,
    box-shadow 0.2s ease,
    color 0.2s ease;
  cursor: pointer;
  font-family: inherit;
}

.sidebar-item:hover {
  border-color: rgba(0, 128, 0, 0.25);
  box-shadow: 0 4px 14px rgba(0, 128, 0, 0.08);
}

.sidebar-item.active {
  background: #008000;
  border-color: #008000;
  color: #fff;
  box-shadow: 0 6px 20px rgba(0, 128, 0, 0.25);
}

.catalog-main {
  background: linear-gradient(180deg, #ffffff 0%, #f8faf8 100%);
  border-radius: 20px;
  padding: clamp(22px, 4vw, 40px);
  border: 1px solid rgba(0, 0, 0, 0.06);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.06);
}

.product-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 14px;
  margin-bottom: 24px;
}

.product-card {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: stretch;
  padding: 0;
  background: #fff;
  border: 1px solid rgba(0, 0, 0, 0.07);
  border-radius: 14px;
  text-decoration: none;
  color: #2d2d2d;
  overflow: hidden;
  transition:
    border-color 0.2s ease,
    box-shadow 0.2s ease,
    transform 0.2s ease;
}

.product-card:hover {
  border-color: rgba(0, 128, 0, 0.35);
  box-shadow: 0 10px 28px rgba(0, 128, 0, 0.12);
  transform: translateY(-3px);
}

.product-card:focus-visible {
  outline: 2px solid #ff7722;
  outline-offset: 2px;
}

.product-card-accent {
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 4px;
  background: linear-gradient(180deg, #008000 0%, #00a344 100%);
  opacity: 0;
  transition: opacity 0.2s ease;
  z-index: 1;
  pointer-events: none;
}

.product-card:hover .product-card-accent,
.product-card:focus-visible .product-card-accent {
  opacity: 1;
}

.product-thumb {
  aspect-ratio: 4 / 3;
  background: linear-gradient(145deg, #ecf3ec 0%, #f4f0ea 55%, #faf8f5 100%);
  position: relative;
}

.product-thumb-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.product-thumb-placeholder {
  height: 100%;
  min-height: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 16px;
  color: #6e8570;
  background-image: radial-gradient(circle at 1px 1px, rgba(0, 128, 0, 0.07) 1px, transparent 0);
  background-size: 18px 18px;
}

.product-thumb-icon {
  width: 44px;
  height: 44px;
  opacity: 0.55;
}

.product-thumb-label {
  font-size: 0.8rem;
  font-weight: 500;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  color: #5c6e5e;
}

.product-card-body {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
  padding: 14px 16px 16px;
}

.product-card-text {
  flex: 1;
  min-width: 0;
  font-size: 0.95rem;
  line-height: 1.4;
}

.product-card-arrow {
  flex-shrink: 0;
  width: 22px;
  height: 22px;
  margin-top: 2px;
  color: #ff7722;
  transition: transform 0.2s ease, color 0.2s ease;
}

.product-card:hover .product-card-arrow {
  transform: translateX(3px);
  color: #e66611;
}

.product-card-arrow svg {
  display: block;
  width: 100%;
  height: 100%;
}

.catalog-placeholder {
  margin: 0 0 24px;
  font-size: 1.05rem;
  line-height: 1.55;
  color: #555;
}

.inline-link {
  color: #008000;
  text-decoration: underline;
  text-underline-offset: 3px;
}

.inline-link:hover {
  color: #006600;
}

.order-button-wrapper {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  align-items: center;
  justify-content: center;
  width: 100%;
}

.order-button {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  background: linear-gradient(135deg, #ff8833 0%, #ff7722 50%, #f06518 100%);
  color: #fff;
  padding: 14px 32px;
  border-radius: 999px;
  text-decoration: none;
  font-size: 1rem;
  font-weight: 600;
  box-shadow: 0 6px 22px rgba(255, 119, 34, 0.35);
  transition:
    transform 0.2s ease,
    box-shadow 0.2s ease,
    filter 0.2s ease;
}

.order-button:hover {
  filter: brightness(1.05);
  box-shadow: 0 8px 28px rgba(255, 119, 34, 0.45);
  transform: translateY(-2px);
}

.catalog-bottom-panel {
  margin-top: 12px;
  margin-bottom: 40px;
  border-radius: 20px;
  padding: clamp(22px, 4vw, 36px);
  background: linear-gradient(
    125deg,
    rgba(0, 128, 0, 0.08) 0%,
    rgba(255, 255, 255, 0.95) 38%,
    rgba(255, 119, 34, 0.1) 100%
  );
  border: 1px solid rgba(0, 128, 0, 0.14);
  box-shadow:
    0 10px 36px rgba(0, 0, 0, 0.06),
    inset 0 1px 0 rgba(255, 255, 255, 0.75);
}

.bottom-panel-inner {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: clamp(20px, 4vw, 36px);
  align-items: center;
}

.bottom-panel-title {
  margin: 0 0 10px;
  font-size: clamp(1.15rem, 2.5vw, 1.35rem);
  color: #008000;
  font-family: var(--font-heading);
  font-weight: 700;
}

.bottom-panel-text {
  margin: 0;
  font-size: 0.95rem;
  line-height: 1.6;
  color: #454545;
  max-width: 52ch;
}

.bottom-panel-actions {
  display: flex;
  flex-direction: column;
  gap: 10px;
  min-width: min(100%, 220px);
}

.bottom-panel-link {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 11px 18px;
  border-radius: 12px;
  font-size: 0.9rem;
  font-weight: 600;
  text-decoration: none;
  text-align: center;
  border: 1px solid rgba(0, 128, 0, 0.25);
  color: #008000;
  background: rgba(255, 255, 255, 0.85);
  transition:
    background 0.2s ease,
    border-color 0.2s ease,
    color 0.2s ease,
    box-shadow 0.2s ease;
}

.bottom-panel-link:hover {
  border-color: #008000;
  box-shadow: 0 4px 14px rgba(0, 128, 0, 0.12);
}

.bottom-panel-link.primary {
  background: #008000;
  border-color: #008000;
  color: #fff;
}

.bottom-panel-link.primary:hover {
  background: #006b00;
  border-color: #006b00;
  box-shadow: 0 6px 18px rgba(0, 128, 0, 0.28);
}

.arrow-icon {
  width: 20px;
  height: 20px;
}

@media (prefers-reduced-motion: reduce) {
  .product-card,
  .product-card-arrow,
  .order-button,
  .sidebar-item {
    transition: none;
  }

  .product-card:hover,
  .order-button:hover {
    transform: none;
  }
}

@media (max-width: 992px) {
  .catalog-layout {
    grid-template-columns: 1fr;
  }

  .catalog-sidebar {
    position: static;
  }

  .sidebar-menu {
    flex-direction: row;
    flex-wrap: wrap;
    gap: 8px;
  }

  .sidebar-item {
    flex: 1 1 auto;
    min-width: min(100%, 160px);
    text-align: center;
  }

  .sidebar-heading {
    text-align: left;
  }
}

@media (max-width: 640px) {
  .catalog-page-header {
    margin-bottom: 20px;
  }

  .product-grid {
    grid-template-columns: 1fr;
  }

  .bottom-panel-inner {
    grid-template-columns: 1fr;
  }

  .bottom-panel-actions {
    flex-direction: row;
    flex-wrap: wrap;
    min-width: 0;
  }

  .bottom-panel-link {
    flex: 1 1 calc(50% - 6px);
    min-width: 140px;
  }
}
</style>