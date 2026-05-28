<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { apiFetch } from '@/api/http'
import { useAuth } from '@/composables/useAuth'
import StaffNewQuotesBanner from '@/components/staff/StaffNewQuotesBanner.vue'
import { CALLBACK_STATUS_OPTIONS, type CallbackDetail } from '@/types/callbacks'

const route = useRoute()
const router = useRouter()
const { isAdministrator } = useAuth()
const callback = ref<CallbackDetail | null>(null)
const loading = ref(true)
const saving = ref(false)
const deleting = ref(false)
const error = ref('')

const siteStatus = ref('new')
const managerNote = ref('')

async function load() {
  loading.value = true
  error.value = ''
  try {
    const ref = encodeURIComponent(String(route.params.ref ?? ''))
    callback.value = await apiFetch<CallbackDetail>(`/staff/callbacks/${ref}/`)
    siteStatus.value = callback.value.site_status
    managerNote.value = callback.value.manager_note
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Не удалось загрузить заявку'
  } finally {
    loading.value = false
  }
}

async function save() {
  if (!callback.value) return
  saving.value = true
  error.value = ''
  try {
    callback.value = await apiFetch<CallbackDetail>(
      `/staff/callbacks/${encodeURIComponent(callback.value.public_number)}/`,
      {
        method: 'PATCH',
        body: JSON.stringify({
          site_status: siteStatus.value,
          manager_note: managerNote.value,
        }),
      },
    )
    siteStatus.value = callback.value.site_status
    managerNote.value = callback.value.manager_note
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Ошибка сохранения'
  } finally {
    saving.value = false
  }
}

function formatDate(iso: string | null) {
  if (!iso) return '—'
  return new Date(iso).toLocaleString('ru-RU')
}

async function removeCallback() {
  if (!callback.value || !confirm(`Удалить заявку ${callback.value.public_number}?`)) return
  deleting.value = true
  error.value = ''
  try {
    await apiFetch(`/staff/callbacks/${encodeURIComponent(callback.value.public_number)}/`, {
      method: 'DELETE',
    })
    await router.push('/staff/inbox?type=callback')
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Не удалось удалить'
  } finally {
    deleting.value = false
  }
}

onMounted(load)
</script>

<template>
  <div class="staff-layout">
    <header class="staff-bar">
      <div class="container staff-bar-inner">
        <button type="button" class="staff-back" @click="router.push('/staff/inbox?type=callback')">
          ← К списку
        </button>
      </div>
    </header>

    <main class="container staff-main">
      <StaffNewQuotesBanner />

      <p v-if="loading" class="staff-muted">Загрузка…</p>
      <p v-else-if="error && !callback" class="staff-error">{{ error }}</p>

      <template v-else-if="callback">
        <div class="detail-header">
          <span class="staff-type-badge staff-type-badge--call">{{ callback.type_label }}</span>
          <h1>{{ callback.public_number }}</h1>
          <p class="detail-subtitle">Клиент заказал обратный звонок с главной страницы (не «Быстрый расчёт»)</p>
        </div>

        <div class="detail-grid">
          <section class="detail-card">
            <h2>Контакты для звонка</h2>
            <dl class="detail-dl">
              <dt>Имя</dt>
              <dd>{{ callback.name }}</dd>
              <dt>Телефон</dt>
              <dd>
                <a :href="`tel:${callback.phone.replace(/\s/g, '')}`">{{ callback.phone }}</a>
              </dd>
              <dt>Создана</dt>
              <dd>{{ formatDate(callback.created_at) }}</dd>
            </dl>
          </section>

          <section class="detail-card">
            <h2>CRM (Битрикс24) — лид</h2>
            <dl class="detail-dl">
              <dt>ID лида</dt>
              <dd>{{ callback.bitrix_lead_id ?? '—' }}</dd>
              <dt>Отправлено</dt>
              <dd>{{ formatDate(callback.bitrix_synced_at) }}</dd>
              <dt v-if="callback.bitrix_stub_path">Файл-заглушка</dt>
              <dd v-if="callback.bitrix_stub_path"><code>{{ callback.bitrix_stub_path }}</code></dd>
              <dt v-if="callback.bitrix_sync_error">Ошибка CRM</dt>
              <dd v-if="callback.bitrix_sync_error" class="staff-error">{{ callback.bitrix_sync_error }}</dd>
            </dl>
          </section>

          <section class="detail-card">
            <h2>На сайте</h2>
            <label class="detail-field">
              <span>Статус</span>
              <select v-model="siteStatus">
                <option
                  v-for="opt in CALLBACK_STATUS_OPTIONS"
                  :key="opt.value"
                  :value="opt.value"
                >
                  {{ opt.label }}
                </option>
              </select>
            </label>
            <label class="detail-field">
              <span>Заметка менеджера</span>
              <textarea v-model="managerNote" rows="4" placeholder="Удобное время, перезвонил…" />
            </label>
            <p v-if="error" class="staff-error">{{ error }}</p>
            <div class="detail-actions">
              <button type="button" class="staff-btn-sm" :disabled="saving" @click="save">
                {{ saving ? 'Сохранение…' : 'Сохранить' }}
              </button>
              <button
                v-if="isAdministrator"
                type="button"
                class="staff-btn-sm staff-btn-sm--danger"
                :disabled="deleting"
                @click="removeCallback"
              >
                {{ deleting ? 'Удаление…' : 'Удалить заявку' }}
              </button>
            </div>
          </section>
        </div>
      </template>
    </main>
  </div>
</template>

<style scoped>
.staff-layout {
  min-height: 100vh;
  background: #f5f5f5;
}
.staff-bar {
  background: #fff;
  border-bottom: 1px solid #e0e0e0;
  padding: 12px 0;
}
.staff-bar-inner {
  display: flex;
  align-items: center;
}
.staff-back {
  background: none;
  border: none;
  color: #666;
  cursor: pointer;
  font-size: 1rem;
}
.staff-main {
  padding: 24px 20px 48px;
  max-width: 1100px;
}
.staff-muted {
  color: #888;
}
.staff-error {
  color: #c62828;
}
.detail-header {
  margin-bottom: 24px;
}
.detail-header h1 {
  font-size: 1.6rem;
}
.detail-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 20px;
}
.detail-card {
  background: #fff;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
}
.detail-card h2 {
  font-size: 1rem;
  margin-bottom: 14px;
  color: #444;
}
.detail-dl {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 8px 16px;
  font-size: 0.95rem;
}
.detail-dl dt {
  color: #888;
}
.detail-field {
  display: flex;
  flex-direction: column;
  gap: 6px;
  margin-bottom: 14px;
}
.detail-field select,
.detail-field textarea {
  padding: 8px 10px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font: inherit;
}
.detail-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}
.staff-btn-sm {
  padding: 8px 16px;
  background: #ff7722;
  color: #fff;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}
.staff-btn-sm--danger {
  background: #c0392b;
}
.staff-btn-sm:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
.staff-type-badge {
  display: inline-block;
  margin-bottom: 8px;
  padding: 4px 10px;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: 600;
}
.staff-type-badge--call {
  background: #fff0e6;
  color: #c45a00;
}
.detail-subtitle {
  margin: 8px 0 0;
  color: #666;
  font-size: 0.95rem;
}
</style>
