<script setup lang="ts">
import { onMounted, onUnmounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { apiFetch } from '@/api/http'
import { useAuth } from '@/composables/useAuth'
import StaffNewQuotesBanner from '@/components/staff/StaffNewQuotesBanner.vue'
import type { ChatDetail, ChatMessage } from '@/types/chats'

const route = useRoute()
const router = useRouter()
const { isAdministrator } = useAuth()
const chat = ref<ChatDetail | null>(null)
const loading = ref(true)
const sending = ref(false)
const deleting = ref(false)
const error = ref('')
const replyText = ref('')
let pollTimer: ReturnType<typeof setInterval> | null = null

function formatDate(iso: string | null) {
  if (!iso) return '—'
  return new Date(iso).toLocaleString('ru-RU')
}

function formatTime(iso: string) {
  return new Date(iso).toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' })
}

function messageClass(msg: ChatMessage) {
  if (msg.sender_type === 'visitor') return 'chat-line--visitor'
  if (msg.sender_type === 'manager') return 'chat-line--manager'
  if (msg.sender_type === 'system') return 'chat-line--system'
  return 'chat-line--bot'
}

function senderLabel(msg: ChatMessage) {
  if (msg.sender_type === 'visitor') return 'Клиент'
  if (msg.sender_type === 'manager') return 'Менеджер'
  if (msg.sender_type === 'system') return 'Система'
  return 'Бот'
}

async function load() {
  const ref = encodeURIComponent(String(route.params.ref ?? ''))
  const data = await apiFetch<ChatDetail>(`/staff/chats/${ref}/`)
  chat.value = data
}

async function loadInitial() {
  loading.value = true
  error.value = ''
  try {
    await load()
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Не удалось загрузить чат'
  } finally {
    loading.value = false
  }
}

async function pollMessages() {
  if (!chat.value) return
  try {
    await load()
  } catch {
    /* ignore poll errors */
  }
}

async function sendReply() {
  if (!chat.value || !replyText.value.trim()) return
  sending.value = true
  error.value = ''
  try {
    chat.value = await apiFetch<ChatDetail>(
      `/staff/chats/${encodeURIComponent(chat.value.public_number)}/reply/`,
      {
        method: 'POST',
        body: JSON.stringify({ text: replyText.value.trim() }),
      },
    )
    replyText.value = ''
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Не удалось отправить'
  } finally {
    sending.value = false
  }
}

async function removeChat() {
  if (!chat.value || !confirm(`Удалить чат ${chat.value.public_number}?`)) return
  deleting.value = true
  error.value = ''
  try {
    await apiFetch(`/staff/chats/${encodeURIComponent(chat.value.public_number)}/`, {
      method: 'DELETE',
    })
    await router.push('/staff/inbox?type=chat')
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Не удалось удалить'
  } finally {
    deleting.value = false
  }
}

onMounted(() => {
  void loadInitial()
  pollTimer = setInterval(() => void pollMessages(), 3000)
})

onUnmounted(() => {
  if (pollTimer) clearInterval(pollTimer)
})
</script>

<template>
  <div class="staff-layout">
    <header class="staff-bar">
      <div class="container staff-bar-inner">
        <button type="button" class="staff-back" @click="router.push('/staff/inbox?type=chat')">
          ← К списку
        </button>
      </div>
    </header>

    <main class="container staff-main">
      <StaffNewQuotesBanner />

      <p v-if="loading" class="staff-muted">Загрузка…</p>
      <p v-else-if="error && !chat" class="staff-error">{{ error }}</p>

      <template v-else-if="chat">
        <div class="detail-header">
          <span class="staff-type-badge staff-type-badge--chat">{{ chat.type_label }}</span>
          <h1>{{ chat.public_number }}</h1>
          <p class="detail-subtitle">
            {{ chat.site_status_display }}
            <span v-if="chat.assigned_to_username"> · {{ chat.assigned_to_username }}</span>
          </p>
          <button
            v-if="isAdministrator"
            type="button"
            class="staff-btn-sm staff-btn-sm--danger"
            :disabled="deleting"
            @click="removeChat"
          >
            {{ deleting ? 'Удаление…' : 'Удалить чат' }}
          </button>
        </div>

        <div class="chat-detail-grid">
          <section class="detail-card chat-transcript-card">
            <h2>Переписка</h2>
            <div class="chat-transcript">
              <div
                v-for="msg in chat.messages"
                :key="msg.id"
                class="chat-line"
                :class="messageClass(msg)"
              >
                <span class="chat-line-sender">{{ senderLabel(msg) }}</span>
                <p class="chat-line-text">{{ msg.text }}</p>
                <span class="chat-line-time">{{ formatTime(msg.created_at) }}</span>
              </div>
            </div>

            <div v-if="chat.site_status !== 'closed'" class="chat-reply-box">
              <p v-if="error" class="staff-error">{{ error }}</p>
              <textarea
                v-model="replyText"
                rows="3"
                placeholder="Ответ клиенту в чат на сайте…"
                @keydown.ctrl.enter="sendReply"
              />
              <button type="button" class="staff-btn-sm" :disabled="sending" @click="sendReply">
                {{ sending ? 'Отправка…' : 'Отправить' }}
              </button>
            </div>
            <p v-else class="staff-muted">Чат закрыт — новые ответы недоступны.</p>
          </section>

          <div class="chat-side">
            <section class="detail-card">
              <h2>Клиент</h2>
              <dl class="detail-dl">
                <dt>Имя</dt>
                <dd>{{ chat.visitor_name || '—' }}</dd>
                <dt>Email</dt>
                <dd>
                  <a v-if="chat.email" :href="`mailto:${chat.email}`">{{ chat.email }}</a>
                  <span v-else>—</span>
                </dd>
                <dt>Телефон</dt>
                <dd>
                  <a v-if="chat.phone" :href="`tel:${chat.phone.replace(/\s/g, '')}`">{{ chat.phone }}</a>
                  <span v-else>—</span>
                </dd>
                <dt>Страница</dt>
                <dd>{{ chat.page_url || '—' }}</dd>
                <dt>Создан</dt>
                <dd>{{ formatDate(chat.created_at) }}</dd>
                <dt>Эскалация</dt>
                <dd>{{ formatDate(chat.escalated_at) }}</dd>
              </dl>
            </section>

            <section class="detail-card">
              <h2>CRM (Битрикс24) — лид</h2>
              <dl class="detail-dl">
                <dt>ID лида</dt>
                <dd>{{ chat.bitrix_lead_id ?? '—' }}</dd>
                <dt>Отправлено</dt>
                <dd>{{ formatDate(chat.bitrix_synced_at) }}</dd>
                <dt v-if="chat.bitrix_stub_path">Файл-заглушка</dt>
                <dd v-if="chat.bitrix_stub_path"><code>{{ chat.bitrix_stub_path }}</code></dd>
                <dt v-if="chat.bitrix_sync_error">Ошибка CRM</dt>
                <dd v-if="chat.bitrix_sync_error" class="staff-error">{{ chat.bitrix_sync_error }}</dd>
              </dl>
              <p v-if="!chat.contact_submitted" class="staff-muted">
                Лид в CRM создаётся после заполнения формы контактов в чате.
              </p>
            </section>
          </div>
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
  max-width: 1200px;
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
.detail-subtitle {
  margin: 8px 0 0;
  color: #666;
}
.chat-detail-grid {
  display: grid;
  grid-template-columns: 1fr minmax(280px, 340px);
  gap: 20px;
  align-items: start;
}
@media (max-width: 900px) {
  .chat-detail-grid {
    grid-template-columns: 1fr;
  }
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
.chat-transcript {
  max-height: 420px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 12px;
  background: #f9f9f9;
  border-radius: 8px;
  margin-bottom: 16px;
}
.chat-line {
  max-width: 85%;
  padding: 10px 14px;
  border-radius: 12px;
  font-size: 0.9rem;
}
.chat-line--visitor {
  align-self: flex-end;
  background: #ff7722;
  color: #fff;
}
.chat-line--manager {
  align-self: flex-start;
  background: #e3f2fd;
  color: #1565c0;
}
.chat-line--bot {
  align-self: flex-start;
  background: #eee;
}
.chat-line--system {
  align-self: center;
  background: #fff8e1;
  color: #795548;
  font-size: 0.85rem;
  max-width: 95%;
  text-align: center;
}
.chat-line-sender {
  display: block;
  font-size: 0.7rem;
  opacity: 0.75;
  margin-bottom: 4px;
}
.chat-line-text {
  margin: 0;
  line-height: 1.45;
  white-space: pre-wrap;
}
.chat-line-time {
  display: block;
  font-size: 0.65rem;
  opacity: 0.65;
  margin-top: 4px;
  text-align: right;
}
.chat-reply-box {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.chat-reply-box textarea {
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font: inherit;
  resize: vertical;
}
.chat-side {
  display: flex;
  flex-direction: column;
  gap: 20px;
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
.staff-btn-sm {
  padding: 8px 16px;
  background: #ff7722;
  color: #fff;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  align-self: flex-start;
}
.staff-btn-sm--danger {
  background: #c0392b;
  margin-top: 12px;
}
.staff-btn-sm:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
.staff-type-badge--chat {
  background: #ede7f6;
  color: #5e35b1;
}
</style>
