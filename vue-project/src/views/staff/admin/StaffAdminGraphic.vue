<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { apiFetch } from '@/api/http'
import StaffAdminShell from '@/components/staff/StaffAdminShell.vue'

type GraphicSettings = {
  banner_title: string
  banner_text: string
  module_title: string
  module_description: string
  max_upload_mb: number
  allowed_formats: string
  ink_limit_percent: number
  black_generation: string
  color_profile: string
  show_promo_banner: boolean
  disclaimer_text: string
}

const form = ref<GraphicSettings | null>(null)
const message = ref('')

async function load() {
  form.value = await apiFetch<GraphicSettings>('/staff/cms/graphic/')
}

async function save() {
  if (!form.value) return
  form.value = await apiFetch<GraphicSettings>('/staff/cms/graphic/', {
    method: 'PUT',
    body: JSON.stringify(form.value),
  })
  message.value = 'Настройки сохранены'
}

onMounted(() => void load())
</script>

<template>
  <StaffAdminShell>
    <h2 class="admin-h2">Графический модуль</h2>
    <p v-if="message" class="admin-ok">{{ message }}</p>

    <form v-if="form" class="admin-card admin-form" @submit.prevent="save">
      <h3>Баннер на странице</h3>
      <label class="admin-label">Заголовок</label>
      <input v-model="form.banner_title" class="admin-inp" />
      <label class="admin-label">Текст</label>
      <textarea v-model="form.banner_text" class="admin-inp" rows="3" />
      <label class="admin-check">
        <input v-model="form.show_promo_banner" type="checkbox" />
        Показывать баннер
      </label>

      <h3 class="admin-h4">Модуль</h3>
      <label class="admin-label">Заголовок</label>
      <input v-model="form.module_title" class="admin-inp" />
      <label class="admin-label">Описание</label>
      <textarea v-model="form.module_description" class="admin-inp" rows="2" />

      <h3 class="admin-h4">Параметры обработки</h3>
      <div class="admin-grid">
        <div>
          <label class="admin-label">Макс. размер файла (МБ)</label>
          <input v-model.number="form.max_upload_mb" type="number" class="admin-inp" min="1" max="50" />
        </div>
        <div>
          <label class="admin-label">Форматы (через запятую)</label>
          <input v-model="form.allowed_formats" class="admin-inp" />
        </div>
        <div>
          <label class="admin-label">Лимит краски (%)</label>
          <input v-model.number="form.ink_limit_percent" type="number" class="admin-inp" />
        </div>
        <div>
          <label class="admin-label">Black generation</label>
          <input v-model="form.black_generation" class="admin-inp" />
        </div>
        <div>
          <label class="admin-label">Цветовой профиль</label>
          <input v-model="form.color_profile" class="admin-inp" />
        </div>
      </div>
      <label class="admin-label">Дисклеймер</label>
      <textarea v-model="form.disclaimer_text" class="admin-inp" rows="2" />

      <button type="submit" class="admin-btn">Сохранить</button>
    </form>
  </StaffAdminShell>
</template>

<style scoped>
@import './admin-shared.css';
.admin-form label {
  display: block;
}
.admin-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 12px;
  margin-bottom: 12px;
}
.admin-check {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 12px 0;
}
</style>
