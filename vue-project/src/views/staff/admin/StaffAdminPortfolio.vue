<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { apiFetch } from '@/api/http'
import StaffAdminShell from '@/components/staff/StaffAdminShell.vue'
import { resolveMediaUrl, uploadCmsImage } from '@/composables/useCmsUpload'

type Work = {
  id: number
  title: string
  image_url: string
  alt_text: string
  sort_order: number
  is_published: boolean
}

const works = ref<Work[]>([])
const loading = ref(true)
const message = ref('')
const error = ref('')
const uploadingId = ref<number | null>(null)

const newWork = ref({
  title: '',
  image_url: '',
  alt_text: '',
})

async function load() {
  loading.value = true
  error.value = ''
  try {
    works.value = await apiFetch<Work[]>('/staff/cms/portfolio/')
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Ошибка загрузки'
  } finally {
    loading.value = false
  }
}

async function saveWork(w: Work) {
  await apiFetch(`/staff/cms/portfolio/${w.id}/`, {
    method: 'PATCH',
    body: JSON.stringify({
      title: w.title,
      image_url: w.image_url,
      alt_text: w.alt_text,
      sort_order: w.sort_order,
      is_published: w.is_published,
    }),
  })
  message.value = 'Сохранено'
}

async function removeWork(w: Work) {
  if (!confirm(`Удалить «${w.title || 'работу'}»?`)) return
  await apiFetch(`/staff/cms/portfolio/${w.id}/`, { method: 'DELETE' })
  await load()
  message.value = 'Удалено'
}

async function addWork() {
  if (!newWork.value.image_url.trim()) {
    error.value = 'Загрузите фото или укажите путь к изображению'
    return
  }
  await apiFetch('/staff/cms/portfolio/', {
    method: 'POST',
    body: JSON.stringify({
      title: newWork.value.title.trim(),
      image_url: newWork.value.image_url.trim(),
      alt_text: newWork.value.alt_text.trim() || newWork.value.title.trim(),
      sort_order: works.value.length,
      is_published: true,
    }),
  })
  newWork.value = { title: '', image_url: '', alt_text: '' }
  await load()
  message.value = 'Работа добавлена'
}

async function onFilePick(w: Work, event: Event) {
  const input = event.target as HTMLInputElement
  const file = input.files?.[0]
  input.value = ''
  if (!file) return
  uploadingId.value = w.id
  error.value = ''
  try {
    w.image_url = await uploadCmsImage(file, 'portfolio')
    await saveWork(w)
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Ошибка загрузки'
  } finally {
    uploadingId.value = null
  }
}

async function onNewFilePick(event: Event) {
  const input = event.target as HTMLInputElement
  const file = input.files?.[0]
  input.value = ''
  if (!file) return
  error.value = ''
  try {
    newWork.value.image_url = await uploadCmsImage(file, 'portfolio')
    if (!newWork.value.title) {
      newWork.value.title = file.name.replace(/\.[^.]+$/, '')
    }
    message.value = 'Фото загружено — нажмите «Добавить»'
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Ошибка загрузки'
  }
}

onMounted(() => {
  void load()
})
</script>

<template>
  <StaffAdminShell>
    <h2 class="admin-h2">Готовые работы</h2>
    <p class="admin-muted">
      Фотографии отображаются на главной между блоками «Быстрый расчёт» и «О компании».
    </p>
    <p v-if="message" class="admin-ok">{{ message }}</p>
    <p v-if="error" class="admin-err">{{ error }}</p>
    <p v-if="loading" class="admin-muted">Загрузка…</p>

    <section v-if="!loading" class="admin-card">
      <div class="portfolio-admin-grid">
        <article v-for="w in works" :key="w.id" class="portfolio-admin-card">
          <div class="portfolio-admin-card__preview">
            <img
              v-if="w.image_url"
              :src="resolveMediaUrl(w.image_url)"
              :alt="w.alt_text || w.title"
            />
            <span v-else class="portfolio-admin-card__empty">Нет фото</span>
          </div>
          <label class="admin-label">Подпись</label>
          <input v-model="w.title" class="admin-inp" />
          <label class="admin-label">Альт-текст</label>
          <input v-model="w.alt_text" class="admin-inp" />
          <label class="admin-label">Порядок</label>
          <input v-model.number="w.sort_order" type="number" class="admin-inp admin-inp--sm" />
          <label class="admin-check">
            <input v-model="w.is_published" type="checkbox" />
            На сайте
          </label>
          <label class="admin-btn-sm admin-btn-sm--file">
            {{ uploadingId === w.id ? 'Загрузка…' : 'Заменить фото' }}
            <input type="file" accept="image/*" hidden @change="onFilePick(w, $event)" />
          </label>
          <div class="portfolio-admin-card__actions">
            <button type="button" class="admin-btn-sm" @click="saveWork(w)">Сохранить</button>
            <button type="button" class="admin-btn-sm admin-btn-sm--danger" @click="removeWork(w)">
              Удалить
            </button>
          </div>
        </article>
      </div>

      <h3 class="admin-h4">Добавить работу</h3>
      <div class="admin-row admin-row--wrap">
        <label class="admin-btn admin-btn--file">
          Загрузить фото
          <input type="file" accept="image/*" hidden @change="onNewFilePick" />
        </label>
        <input v-model="newWork.title" class="admin-inp" placeholder="Подпись" />
        <input v-model="newWork.alt_text" class="admin-inp" placeholder="Альт-текст (необяз.)" />
        <button type="button" class="admin-btn" :disabled="!newWork.image_url" @click="addWork">
          Добавить
        </button>
      </div>
      <p v-if="newWork.image_url" class="admin-muted">Файл: {{ newWork.image_url }}</p>
    </section>
  </StaffAdminShell>
</template>

<style scoped>
@import './admin-shared.css';

.portfolio-admin-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 20px;
  margin-bottom: 24px;
}

.portfolio-admin-card {
  border: 1px solid #e8e8e8;
  border-radius: 10px;
  padding: 12px;
  background: #fafafa;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.portfolio-admin-card__preview {
  aspect-ratio: 4 / 3;
  border-radius: 8px;
  overflow: hidden;
  background: #ddd;
}

.portfolio-admin-card__preview img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.portfolio-admin-card__empty {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #888;
  font-size: 0.9rem;
}

.portfolio-admin-card__actions {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.admin-label {
  font-size: 0.8rem;
  color: #666;
}

.admin-check {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.9rem;
}

.admin-btn-sm--file,
.admin-btn--file {
  cursor: pointer;
  display: inline-flex;
  align-items: center;
}

.admin-btn-sm--danger {
  background: #fee;
  color: #c62828;
}

.admin-row--wrap {
  flex-wrap: wrap;
}
</style>
