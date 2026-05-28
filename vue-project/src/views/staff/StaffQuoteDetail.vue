<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { apiFetch } from '@/api/http'
import { useAuth } from '@/composables/useAuth'
import StaffNewQuotesBanner from '@/components/staff/StaffNewQuotesBanner.vue'
import { quoteParamLabel } from '@/data/quoteParamLabels'
import { SITE_STATUS_OPTIONS, type QuoteAttachmentItem, type QuoteDetail } from '@/types/quotes'

const route = useRoute()
const router = useRouter()
const { isAdministrator } = useAuth()
const quote = ref<QuoteDetail | null>(null)
const loading = ref(true)
const saving = ref(false)
const deleting = ref(false)
const error = ref('')

const siteStatus = ref('new')
const managerNote = ref('')

const paramRows = computed(() => {
  if (quote.value?.parameters_labeled?.length) {
    return quote.value.parameters_labeled
  }
  if (!quote.value?.parameters) return []
  return Object.entries(quote.value.parameters).map(([key, value]) => ({
    key,
    label: quoteParamLabel(key),
    value: String(value),
  }))
})

async function load() {
  loading.value = true
  error.value = ''
  try {
    const ref = encodeURIComponent(String(route.params.ref ?? ''))
    quote.value = await apiFetch<QuoteDetail>(`/staff/quotes/${ref}/`)
    siteStatus.value = quote.value.site_status
    managerNote.value = quote.value.manager_note
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Не удалось загрузить заявку'
  } finally {
    loading.value = false
  }
}

async function save() {
  if (!quote.value) return
  saving.value = true
  error.value = ''
  try {
    quote.value = await apiFetch<QuoteDetail>(
      `/staff/quotes/${encodeURIComponent(quote.value.public_number)}/`,
      {
        method: 'PATCH',
        body: JSON.stringify({
          site_status: siteStatus.value,
          manager_note: managerNote.value,
        }),
      },
    )
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

function formatFileSize(bytes: number) {
  if (bytes < 1024) return `${bytes} Б`
  if (bytes < 1024 * 1024) return `${Math.round(bytes / 1024)} КБ`
  return `${(bytes / (1024 * 1024)).toFixed(1)} МБ`
}

function attachmentPreviewUrl(att: QuoteAttachmentItem) {
  return `${att.download_url}?inline=1`
}

async function removeQuote() {
  if (!quote.value || !confirm(`Удалить заявку ${quote.value.public_number}?`)) return
  deleting.value = true
  error.value = ''
  try {
    await apiFetch(`/staff/quotes/${encodeURIComponent(quote.value.public_number)}/`, {
      method: 'DELETE',
    })
    await router.push('/staff/inbox?type=quote')
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
        <button type="button" class="staff-back" @click="router.push('/staff/inbox?type=quote')">
          ← К списку
        </button>
      </div>
    </header>

    <main class="container staff-main">
      <StaffNewQuotesBanner />

      <p v-if="loading" class="staff-muted">Загрузка…</p>
      <p v-else-if="error && !quote" class="staff-error">{{ error }}</p>

      <template v-else-if="quote">
        <div class="detail-header">
          <h1>{{ quote.public_number }}</h1>
          <span class="detail-service">{{ quote.service_title }}</span>
        </div>

        <div class="detail-grid">
          <section class="detail-card">
            <h2>Спецификация</h2>
            <dl class="detail-dl">
              <template v-for="row in paramRows" :key="row.key">
                <dt>{{ row.label }}</dt>
                <dd>{{ row.value }}</dd>
              </template>
            </dl>
            <p v-if="quote.client_comment" class="detail-comment">
              <strong>Комментарий клиента:</strong> {{ quote.client_comment }}
            </p>
          </section>

          <section v-if="quote.attachments?.length" class="detail-card detail-card--wide">
            <h2>Макеты</h2>
            <div class="attachment-grid">
              <div v-for="att in quote.attachments" :key="att.id" class="attachment-card">
                <a
                  v-if="att.is_image"
                  :href="attachmentPreviewUrl(att)"
                  class="attachment-preview-link"
                  target="_blank"
                  rel="noopener"
                >
                  <img :src="attachmentPreviewUrl(att)" :alt="att.original_name" class="attachment-thumb" />
                </a>
                <div v-else class="attachment-file-icon" aria-hidden="true">📄</div>
                <p class="attachment-name">{{ att.original_name }}</p>
                <p class="attachment-meta">{{ formatFileSize(att.file_size) }}</p>
                <a :href="att.download_url" class="attachment-download" download>
                  Скачать
                </a>
              </div>
            </div>
          </section>

          <section class="detail-card">
            <h2>Контакты</h2>
            <dl class="detail-dl">
              <dt>Заказчик</dt>
              <dd>
                {{ quote.company_type_display }}
                <template v-if="quote.company_name"> — {{ quote.company_name }}</template>
              </dd>
              <dt v-if="quote.inn">ИНН</dt>
              <dd v-if="quote.inn">{{ quote.inn }}</dd>
              <dt>Контакт</dt>
              <dd>{{ quote.contact_name }}</dd>
              <dt>Телефон</dt>
              <dd>{{ quote.contact_phone }}</dd>
              <dt>Email</dt>
              <dd><a :href="`mailto:${quote.contact_email}`">{{ quote.contact_email }}</a></dd>
            </dl>
          </section>

          <section class="detail-card">
            <h2>CRM (Битрикс24)</h2>
            <dl class="detail-dl">
              <dt>ID в CRM</dt>
              <dd>{{ quote.bitrix_lead_id ?? '—' }}</dd>
              <dt>Отправлено</dt>
              <dd>{{ formatDate(quote.bitrix_synced_at) }}</dd>
              <dt v-if="quote.bitrix_stub_path">Файл-заглушка</dt>
              <dd v-if="quote.bitrix_stub_path"><code>{{ quote.bitrix_stub_path }}</code></dd>
              <dt v-if="quote.bitrix_stub_path && quote.bitrix_lead_id && quote.bitrix_lead_id >= 10000">
                Режим
              </dt>
              <dd
                v-if="quote.bitrix_stub_path && quote.bitrix_lead_id && quote.bitrix_lead_id >= 10000"
                class="staff-warn"
              >
                В CRM не отправлено — только локальная копия (файл-заглушка). См. ошибку ниже.
              </dd>
              <dt v-if="quote.bitrix_sync_error">Ошибка CRM</dt>
              <dd v-if="quote.bitrix_sync_error" class="staff-error">{{ quote.bitrix_sync_error }}</dd>
            </dl>
          </section>

          <section class="detail-card">
            <h2>На сайте</h2>
            <label class="detail-field">
              <span>Статус</span>
              <select v-model="siteStatus">
                <option v-for="opt in SITE_STATUS_OPTIONS" :key="opt.value" :value="opt.value">
                  {{ opt.label }}
                </option>
              </select>
            </label>
            <label class="detail-field">
              <span>Заметка менеджера</span>
              <textarea v-model="managerNote" rows="4" placeholder="Перед выездом, уточнения…" />
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
                @click="removeQuote"
              >
                {{ deleting ? 'Удаление…' : 'Удалить заявку' }}
              </button>
            </div>
          </section>
        </div>

        <p class="detail-meta">Создана: {{ formatDate(quote.created_at) }}</p>
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
.detail-header {
  margin-bottom: 24px;
}
.detail-header h1 {
  font-size: 1.6rem;
}
.detail-service {
  color: #666;
}
.detail-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 20px;
}
.detail-card--wide {
  grid-column: 1 / -1;
}
.attachment-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
}
.attachment-card {
  width: 160px;
  padding: 12px;
  border: 1px solid #e8e8e8;
  border-radius: 10px;
  background: #fafafa;
  text-align: center;
}
.attachment-thumb {
  width: 100%;
  height: 120px;
  object-fit: cover;
  border-radius: 8px;
  display: block;
}
.attachment-file-icon {
  font-size: 48px;
  line-height: 120px;
  height: 120px;
}
.attachment-name {
  font-size: 13px;
  font-weight: 600;
  margin: 8px 0 4px;
  word-break: break-word;
}
.attachment-meta {
  font-size: 12px;
  color: #888;
  margin: 0 0 8px;
}
.attachment-download {
  font-size: 13px;
  color: #ff7722;
  font-weight: 600;
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
  font-size: 0.9rem;
}
.detail-dl dt {
  color: #888;
}
.detail-dl dd {
  margin: 0;
  word-break: break-word;
}
.detail-comment {
  margin-top: 14px;
  font-size: 0.9rem;
  line-height: 1.5;
}
.detail-field {
  display: block;
  margin-bottom: 14px;
}
.detail-field span {
  display: block;
  margin-bottom: 6px;
  font-size: 0.9rem;
}
.detail-field select,
.detail-field textarea {
  width: 100%;
  padding: 8px 10px;
  border: 1px solid #ddd;
  border-radius: 6px;
}
.detail-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}
.staff-btn-sm {
  padding: 10px 20px;
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
.staff-error {
  color: #c0392b;
  font-size: 0.9rem;
}
.staff-warn {
  color: #b35c00;
  font-size: 0.9rem;
}
.staff-muted {
  color: #888;
}
.detail-meta {
  margin-top: 20px;
  color: #999;
  font-size: 0.85rem;
}
code {
  font-size: 0.8rem;
  word-break: break-all;
}
</style>
