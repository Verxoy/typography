<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { apiFetch } from '@/api/http'
import { useAuth } from '@/composables/useAuth'
import StaffNewQuotesBanner from '@/components/staff/StaffNewQuotesBanner.vue'
import { SITE_STATUS_OPTIONS, type QuoteListItem } from '@/types/quotes'

const router = useRouter()
const { user, logout } = useAuth()

const quotes = ref<QuoteListItem[]>([])
const loading = ref(true)
const search = ref('')
const statusFilter = ref('')

async function load() {
  loading.value = true
  try {
    const params = new URLSearchParams()
    if (search.value.trim()) params.set('search', search.value.trim())
    if (statusFilter.value) params.set('status', statusFilter.value)
    const q = params.toString()
    const query = q ? `?${q}` : ''
    quotes.value = await apiFetch<QuoteListItem[]>(`/staff/quotes/${query}`)
  } finally {
    loading.value = false
  }
}

onMounted(load)

async function doLogout() {
  await logout()
  router.push('/staff/login')
}

function formatDate(iso: string) {
  return new Date(iso).toLocaleString('ru-RU', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

function statusLabel(code: string) {
  return SITE_STATUS_OPTIONS.find((o) => o.value === code)?.label ?? code
}
</script>

<template>
  <div class="staff-layout">
    <header class="staff-bar">
      <div class="container staff-bar-inner">
        <div>
          <h1>Заявки «Быстрый расчёт»</h1>
          <p v-if="user" class="staff-user">{{ user.first_name || user.username }}</p>
        </div>
        <div class="staff-bar-actions">
          <router-link to="/quick-quote" class="staff-link-btn">Форма расчёта</router-link>
          <router-link to="/" class="staff-link-btn">Сайт</router-link>
          <button type="button" class="staff-link-btn" @click="doLogout">Выйти</button>
        </div>
      </div>
    </header>

    <main class="container staff-main">
      <StaffNewQuotesBanner />

      <div class="staff-filters">
        <input
          v-model="search"
          type="search"
          placeholder="Поиск: номер, ИНН, компания, телефон…"
          @keyup.enter="load"
        />
        <select v-model="statusFilter" @change="load">
          <option value="">Все статусы</option>
          <option v-for="opt in SITE_STATUS_OPTIONS" :key="opt.value" :value="opt.value">
            {{ opt.label }}
          </option>
        </select>
        <button type="button" class="staff-btn-sm" @click="load">Найти</button>
      </div>

      <p v-if="loading" class="staff-muted">Загрузка…</p>
      <p v-else-if="!quotes.length" class="staff-muted">Заявок пока нет</p>

      <div v-else class="staff-table-wrap">
        <table class="staff-table">
          <thead>
            <tr>
              <th>Номер</th>
              <th>Услуга</th>
              <th>Организация</th>
              <th>ИНН</th>
              <th>Контакт</th>
              <th>Макет</th>
              <th>Статус</th>
              <th>CRM</th>
              <th>Дата</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="q in quotes"
              :key="q.id"
              class="staff-row"
              @click="router.push(`/staff/quotes/${encodeURIComponent(q.public_number)}`)"
            >
              <td><strong>{{ q.public_number }}</strong></td>
              <td>{{ q.service_title }}</td>
              <td>{{ q.company_name }}</td>
              <td>{{ q.inn }}</td>
              <td>{{ q.contact_name }}<br /><small>{{ q.contact_phone }}</small></td>
              <td>{{ q.has_attachments ? '✓' : '—' }}</td>
              <td>{{ statusLabel(q.site_status) }}</td>
              <td>
                <span v-if="q.bitrix_synced_at" class="crm-ok">✓</span>
                <span v-else class="crm-no">—</span>
              </td>
              <td>{{ formatDate(q.created_at) }}</td>
            </tr>
          </tbody>
        </table>
      </div>
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
  padding: 16px 0;
}
.staff-bar-inner {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 16px;
}
.staff-bar h1 {
  font-size: 1.35rem;
}
.staff-user {
  color: #666;
  font-size: 0.85rem;
}
.staff-bar-actions {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}
.staff-link-btn {
  padding: 8px 14px;
  background: #eee;
  border: none;
  border-radius: 6px;
  text-decoration: none;
  color: #333;
  font-size: 0.9rem;
  cursor: pointer;
}
.staff-main {
  padding: 24px 20px 48px;
}
.staff-filters {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}
.staff-filters input,
.staff-filters select {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  flex: 1;
  min-width: 160px;
}
.staff-btn-sm {
  padding: 8px 16px;
  background: #ff7722;
  color: #fff;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}
.staff-table-wrap {
  overflow-x: auto;
  background: #fff;
  border-radius: 10px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
}
.staff-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.9rem;
}
.staff-table th,
.staff-table td {
  padding: 12px 14px;
  text-align: left;
  border-bottom: 1px solid #eee;
}
.staff-table th {
  background: #fafafa;
  font-weight: 600;
  color: #444;
}
.staff-row {
  cursor: pointer;
}
.staff-row:hover {
  background: #fff8f3;
}
.crm-ok {
  color: #00aa44;
  font-weight: bold;
}
.crm-no {
  color: #aaa;
}
.staff-muted {
  color: #888;
}
</style>
