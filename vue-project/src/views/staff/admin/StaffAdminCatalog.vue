<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { apiFetch } from '@/api/http'
import StaffAdminShell from '@/components/staff/StaffAdminShell.vue'
import { resolveMediaUrl, uploadCmsImage } from '@/composables/useCmsUpload'
import { HOME_CATALOG_SECTION_TITLES } from '@/data/homeCatalogSections'

type Section = {
  id: number
  section_id: string
  title: string
  home_image_url: string
  sort_order: number
  is_published: boolean
}

type Product = {
  id: number
  section: number
  section_id: string
  section_title: string
  title: string
  slug: string
  image_url: string
  sort_order: number
  is_published: boolean
}

const sections = ref<Section[]>([])
const products = ref<Product[]>([])
const loading = ref(true)
const message = ref('')
const error = ref('')
const expandedSectionId = ref<number | null>(null)
const uploadingSectionId = ref<number | null>(null)
const uploadingProductId = ref<number | null>(null)

const orderedSections = computed(() => {
  const byTitle = new Map(sections.value.map((s) => [s.title, s]))
  return HOME_CATALOG_SECTION_TITLES.map((title) => byTitle.get(title)).filter(
    (s): s is Section => Boolean(s),
  )
})

function productsInSection(sectionId: number) {
  return products.value
    .filter((p) => p.section === sectionId)
    .sort((a, b) => a.sort_order - b.sort_order || a.title.localeCompare(b.title, 'ru'))
}

function toggleSection(sectionId: number) {
  expandedSectionId.value = expandedSectionId.value === sectionId ? null : sectionId
}

async function load() {
  loading.value = true
  error.value = ''
  try {
    sections.value = await apiFetch<Section[]>('/staff/cms/catalog/sections/')
    products.value = await apiFetch<Product[]>('/staff/cms/catalog/products/')
    if (!expandedSectionId.value && sections.value.length) {
      const first =
        HOME_CATALOG_SECTION_TITLES.map((title) =>
          sections.value.find((s) => s.title === title),
        ).find(Boolean) ?? sections.value[0]
      expandedSectionId.value = first.id
    }
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Ошибка загрузки'
  } finally {
    loading.value = false
  }
}

async function saveSectionHome(s: Section) {
  await apiFetch(`/staff/cms/catalog/sections/${s.id}/`, {
    method: 'PATCH',
    body: JSON.stringify({ home_image_url: s.home_image_url }),
  })
  message.value = `Сохранено: ${s.title}`
}

async function onSectionImagePick(s: Section, event: Event) {
  const input = event.target as HTMLInputElement
  const file = input.files?.[0]
  input.value = ''
  if (!file) return
  uploadingSectionId.value = s.id
  error.value = ''
  try {
    s.home_image_url = await uploadCmsImage(file, 'catalog')
    await saveSectionHome(s)
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Ошибка загрузки'
  } finally {
    uploadingSectionId.value = null
  }
}

async function saveProductImage(p: Product) {
  await apiFetch(`/staff/cms/catalog/products/${p.id}/`, {
    method: 'PATCH',
    body: JSON.stringify({ image_url: p.image_url }),
  })
  message.value = `Фото сохранено: ${p.title}`
}

async function onProductImagePick(p: Product, event: Event) {
  const input = event.target as HTMLInputElement
  const file = input.files?.[0]
  input.value = ''
  if (!file) return
  uploadingProductId.value = p.id
  error.value = ''
  try {
    p.image_url = await uploadCmsImage(file, 'catalog')
    await saveProductImage(p)
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Ошибка загрузки'
  } finally {
    uploadingProductId.value = null
  }
}

onMounted(() => {
  void load()
})
</script>

<template>
  <StaffAdminShell>
    <h2 class="admin-h2">Каталог — фотографии</h2>
    <p class="admin-muted catalog-intro">
      Выберите раздел, чтобы изменить фото карточки на главной странице и фото всех подразделов в каталоге.
      Нажмите «Загрузить фото» или укажите путь к файлу, затем «Сохранить».
    </p>
    <p v-if="message" class="admin-ok">{{ message }}</p>
    <p v-if="error" class="admin-err">{{ error }}</p>
    <p v-if="loading" class="admin-muted">Загрузка…</p>

    <div v-if="!loading" class="catalog-sections">
      <article
        v-for="section in orderedSections"
        :key="section.id"
        class="catalog-block"
        :class="{ 'catalog-block--open': expandedSectionId === section.id }"
      >
        <button type="button" class="catalog-block__head" @click="toggleSection(section.id)">
          <span class="catalog-block__chevron">{{ expandedSectionId === section.id ? '▼' : '▶' }}</span>
          <span class="catalog-block__title">{{ section.title }}</span>
          <span class="catalog-block__count">
            {{ productsInSection(section.id).length }} подразделов
          </span>
        </button>

        <div v-show="expandedSectionId === section.id" class="catalog-block__body">
          <section class="catalog-home-card">
            <h4 class="catalog-subtitle">Карточка на главной странице</h4>
            <div class="catalog-home-row">
              <div class="catalog-preview catalog-preview--home">
                <img
                  v-if="section.home_image_url"
                  :src="resolveMediaUrl(section.home_image_url)"
                  :alt="section.title"
                />
                <span v-else class="catalog-preview__empty">Нет фото</span>
              </div>
              <div class="catalog-home-actions">
                <label class="admin-btn admin-btn--file">
                  {{ uploadingSectionId === section.id ? 'Загрузка…' : 'Загрузить фото' }}
                  <input type="file" accept="image/*" hidden @change="onSectionImagePick(section, $event)" />
                </label>
                <input
                  v-model="section.home_image_url"
                  class="admin-inp"
                  placeholder="/images/… или /media/catalog/…"
                />
                <button type="button" class="admin-btn-sm" @click="saveSectionHome(section)">
                  Сохранить
                </button>
              </div>
            </div>
          </section>

          <section class="catalog-products-block">
            <h4 class="catalog-subtitle">Подразделы в каталоге</h4>
            <p v-if="!productsInSection(section.id).length" class="admin-muted">
              В этом разделе пока нет позиций.
            </p>
            <ul v-else class="catalog-product-list">
              <li v-for="p in productsInSection(section.id)" :key="p.id" class="catalog-product-item">
                <div class="catalog-preview catalog-preview--product">
                  <img
                    v-if="p.image_url"
                    :src="resolveMediaUrl(p.image_url)"
                    :alt="p.title"
                  />
                  <span v-else class="catalog-preview__empty">Нет фото</span>
                </div>
                <div class="catalog-product-info">
                  <p class="catalog-product-name">{{ p.title }}</p>
                  <input
                    v-model="p.image_url"
                    class="admin-inp admin-inp--compact"
                    placeholder="Путь к изображению"
                  />
                  <div class="catalog-product-actions">
                    <label class="admin-btn-sm admin-btn-sm--file">
                      {{ uploadingProductId === p.id ? '…' : 'Загрузить' }}
                      <input type="file" accept="image/*" hidden @change="onProductImagePick(p, $event)" />
                    </label>
                    <button type="button" class="admin-btn-sm" @click="saveProductImage(p)">
                      Сохранить
                    </button>
                  </div>
                </div>
              </li>
            </ul>
          </section>
        </div>
      </article>
    </div>
  </StaffAdminShell>
</template>

<style scoped>
@import './admin-shared.css';

.catalog-intro {
  max-width: 720px;
  margin-bottom: 20px;
}

.catalog-sections {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.catalog-block {
  background: #fff;
  border: 1px solid #e8e8e8;
  border-radius: 12px;
  overflow: hidden;
}

.catalog-block--open {
  border-color: #f72;
  box-shadow: 0 4px 20px rgba(255, 119, 34, 0.08);
}

.catalog-block__head {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 16px;
  background: #fafafa;
  border: none;
  cursor: pointer;
  text-align: left;
  font: inherit;
}

.catalog-block__head:hover {
  background: #f3f3f3;
}

.catalog-block__chevron {
  color: #f72;
  font-size: 0.75rem;
  width: 1rem;
}

.catalog-block__title {
  flex: 1;
  font-weight: 600;
  font-size: 1rem;
  color: #222;
}

.catalog-block__count {
  font-size: 0.85rem;
  color: #888;
}

.catalog-block__body {
  padding: 16px 20px 20px;
  border-top: 1px solid #eee;
}

.catalog-subtitle {
  margin: 0 0 12px;
  font-size: 0.95rem;
  font-weight: 600;
  color: #444;
}

.catalog-home-card {
  margin-bottom: 24px;
  padding-bottom: 20px;
  border-bottom: 1px dashed #e0e0e0;
}

.catalog-home-row {
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
  align-items: flex-start;
}

.catalog-home-actions {
  flex: 1;
  min-width: 220px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.catalog-preview {
  border-radius: 10px;
  overflow: hidden;
  background: #eee;
  flex-shrink: 0;
}

.catalog-preview--home {
  width: 200px;
  height: 140px;
}

.catalog-preview--product {
  width: 88px;
  height: 88px;
}

.catalog-preview img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.catalog-preview__empty {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
  font-size: 0.8rem;
  color: #999;
}

.catalog-product-list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.catalog-product-item {
  display: flex;
  gap: 14px;
  align-items: flex-start;
  padding: 12px;
  background: #fafafa;
  border-radius: 10px;
  border: 1px solid #eee;
}

.catalog-product-info {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.catalog-product-name {
  margin: 0;
  font-weight: 600;
  font-size: 0.95rem;
  color: #333;
}

.catalog-product-actions {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.admin-inp--compact {
  font-size: 0.85rem;
}

.admin-btn--file,
.admin-btn-sm--file {
  cursor: pointer;
  display: inline-flex;
  align-items: center;
}

@media (max-width: 600px) {
  .catalog-home-row {
    flex-direction: column;
  }

  .catalog-preview--home {
    width: 100%;
    max-width: 280px;
  }

  .catalog-product-item {
    flex-direction: column;
  }
}
</style>
