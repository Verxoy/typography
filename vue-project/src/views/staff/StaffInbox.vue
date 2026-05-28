<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { apiFetch } from '@/api/http'
import { useAuth } from '@/composables/useAuth'
import StaffNewQuotesBanner from '@/components/staff/StaffNewQuotesBanner.vue'
import { CALLBACK_STATUS_OPTIONS } from '@/types/callbacks'
import { CHAT_STATUS_OPTIONS } from '@/types/chats'
import { SITE_STATUS_OPTIONS } from '@/types/quotes'
import type { InboxListItem, InboxTypeFilter } from '@/types/inbox'

const route = useRoute()
const router = useRouter()
const { user, logout } = useAuth()

const items = ref<InboxListItem[]>([])
const loading = ref(true)
const search = ref('')
const statusFilter = ref('')
const typeFilter = ref<InboxTypeFilter>('')

const pageTitle = computed(() => {
  if (typeFilter.value === 'quote') return 'Заявки «Быстрый расчёт»'
  if (typeFilter.value === 'callback') return 'Заявки «Заказ звонка»'
  if (typeFilter.value === 'chat') return 'Чаты с сайта'
  return 'Все заявки с сайта'
})

function syncTypeFromRoute() {
  const t = String(route.query.type ?? '')
  typeFilter.value = t === 'quote' || t === 'callback' || t === 'chat' ? t : ''
}

async function load() {
  loading.value = true
  try {
    const params = new URLSearchParams()
    if (typeFilter.value) params.set('type', typeFilter.value)
    if (search.value.trim()) params.set('search', search.value.trim())
    if (statusFilter.value) params.set('status', statusFilter.value)
    const q = params.toString()
    items.value = await apiFetch<InboxListItem[]>(`/staff/inbox/${q ? `?${q}` : ''}`)
  } finally {
    loading.value = false
  }
}

function setTypeFilter(value: InboxTypeFilter) {
  typeFilter.value = value
  const query = value ? { type: value } : {}
  router.replace({ path: '/staff/inbox', query })
  void load()
}

function openItem(row: InboxListItem) {
  const ref = encodeURIComponent(row.public_number)
  if (row.request_type === 'callback') {
    router.push(`/staff/callbacks/${ref}`)
  } else if (row.request_type === 'chat') {
    router.push(`/staff/chats/${ref}`)
  } else {
    router.push(`/staff/quotes/${ref}`)
  }
}

onMounted(() => {
  syncTypeFromRoute()
  void load()
})

watch(
  () => route.query.type,
  () => {
    syncTypeFromRoute()
    void load()
  },
)

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

const statusOptions = computed(() => {
  if (typeFilter.value === 'callback') return CALLBACK_STATUS_OPTIONS
  if (typeFilter.value === 'chat') return CHAT_STATUS_OPTIONS
  if (typeFilter.value === 'quote') return SITE_STATUS_OPTIONS
  return [
    ...SITE_STATUS_OPTIONS,
    ...CALLBACK_STATUS_OPTIONS.filter(
      (c) => !SITE_STATUS_OPTIONS.some((q) => q.value === c.value),
    ),
    ...CHAT_STATUS_OPTIONS.filter(
      (c) =>
        !SITE_STATUS_OPTIONS.some((q) => q.value === c.value) &&
        !CALLBACK_STATUS_OPTIONS.some((cb) => cb.value === c.value),
    ),
  ]
})

function statusLabel(row: InboxListItem) {
  const opts =
    row.request_type === 'callback'
      ? CALLBACK_STATUS_OPTIONS
      : row.request_type === 'chat'
        ? CHAT_STATUS_OPTIONS
        : SITE_STATUS_OPTIONS
  return opts.find((o) => o.value === row.site_status)?.label ?? row.site_status
}

function contactPhone(row: InboxListItem) {
  return row.phone ?? row.contact_phone ?? '—'
}
</script>

<template>
  <div class="staff-layout">
    <header class="staff-bar">
      <div class="container staff-bar-inner">
        <div>
          <h1>{{ pageTitle }}</h1>
          <p v-if="user" class="staff-user">{{ user.first_name || user.username }}</p>
        </div>
        <div class="staff-bar-actions">
          <router-link to="/staff/admin" class="staff-link-btn">Управление сайтом</router-link>
          <router-link to="/quick-quote" class="staff-link-btn">Форма расчёта</router-link>
          <router-link to="/#callback" class="staff-link-btn">Форма звонка</router-link>
          <router-link to="/" class="staff-link-btn">Сайт</router-link>
          <button type="button" class="staff-link-btn" @click="doLogout">Выйти</button>
        </div>
      </div>
    </header>

    <main class="container staff-main">
      <StaffNewQuotesBanner />

      <div class="staff-type-tabs" role="tablist">
        <button
          type="button"
          :class="['staff-type-tab', { active: !typeFilter }]"
          @click="setTypeFilter('')"
        >
          Все
        </button>
        <button
          type="button"
          :class="['staff-type-tab', { active: typeFilter === 'quote' }]"
          @click="setTypeFilter('quote')"
        >
          Быстрый расчёт
        </button>
        <button
          type="button"
          :class="['staff-type-tab', { active: typeFilter === 'callback' }]"
          @click="setTypeFilter('callback')"
        >
          Заказ звонка
        </button>
        <button
          type="button"
          :class="['staff-type-tab', { active: typeFilter === 'chat' }]"
          @click="setTypeFilter('chat')"
        >
          Чаты
        </button>
      </div>

      <div class="staff-filters">
        <input
          v-model="search"
          type="search"
          placeholder="Поиск: номер, имя, телефон, ИНН…"
          @keyup.enter="load"
        />
        <select v-model="statusFilter" @change="load">
          <option value="">Все статусы</option>
          <option v-for="opt in statusOptions" :key="opt.value" :value="opt.value">
            {{ opt.label }}
          </option>
        </select>
        <button type="button" class="staff-btn-sm" @click="load">Найти</button>
      </div>

      <p v-if="loading" class="staff-muted">Загрузка…</p>
      <p v-else-if="!items.length" class="staff-muted">Заявок пока нет</p>

      <div v-else class="staff-table-wrap">
        <table class="staff-table">
          <thead>
            <tr>
              <th>Тип</th>
              <th>Номер</th>
              <th>Суть</th>
              <th>Контакт</th>
              <th>Телефон</th>
              <th v-if="!typeFilter || typeFilter === 'quote' || typeFilter === 'all'">Макет</th>
              <th>Статус</th>
              <th>CRM</th>
              <th>Дата</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="row in items"
              :key="`${row.request_type}-${row.id}`"
              class="staff-row"
              @click="openItem(row)"
            >
              <td>
                <span
                  class="staff-type-badge"
                  :class="{
                    'staff-type-badge--call': row.request_type === 'callback',
                    'staff-type-badge--quote': row.request_type === 'quote',
                    'staff-type-badge--chat': row.request_type === 'chat',
                  }"
                >
                  {{ row.type_label }}
                </span>
              </td>
              <td><strong>{{ row.public_number }}</strong></td>
              <td>{{ row.title }}</td>
              <td>{{ row.contact_name || '—' }}</td>
              <td>{{ contactPhone(row) }}</td>
              <td v-if="!typeFilter || typeFilter === 'quote' || typeFilter === 'all'">
                <template v-if="row.request_type === 'quote'">
                  {{ row.has_attachments ? '✓' : '—' }}
                </template>
                <template v-else>—</template>
              </td>
              <td>{{ statusLabel(row) }}</td>
              <td>
                <span v-if="row.bitrix_synced_at" class="staff-crm-ok">✓</span>
                <span v-else-if="row.request_type === 'chat' && !row.contact_submitted" class="staff-muted">форма</span>
                <span v-else class="staff-muted">—</span>
              </td>
              <td>{{ formatDate(row.created_at) }}</td>
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
.staff-crm-ok {
  color: #00aa44;
  font-weight: bold;
}
.staff-muted {
  color: #888;
}
.staff-type-tabs {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 16px;
}
.staff-type-tab {
  padding: 8px 16px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background: #fff;
  cursor: pointer;
  font-size: 0.9rem;
}
.staff-type-tab.active {
  border-color: #ff7722;
  background: #fff5ee;
  color: #c45a00;
  font-weight: 600;
}
.staff-type-badge {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 600;
  white-space: nowrap;
}
.staff-type-badge--quote {
  background: #e8f4ff;
  color: #1a5a9e;
}
.staff-type-badge--call {
  background: #fff0e6;
  color: #c45a00;
}
.staff-type-badge--chat {
  background: #ede7f6;
  color: #5e35b1;
}
</style>
