<script setup lang="ts">
import { computed, nextTick, onMounted, onUnmounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { apiFetch } from '@/api/http'
import type { ChatMessage, ChatSessionPublic, ChatStatus } from '@/types/chats'

const STORAGE_KEY = 'chat_session_key'
const PHONE_PREFIX = '+7'

const route = useRoute()
const isOpen = ref(false)
const message = ref('')
const loading = ref(false)
const sessionKey = ref('')
const sessionStatus = ref<ChatStatus>('bot')
const messages = ref<ChatMessage[]>([])
const contactSubmitted = ref(false)
const contactError = ref('')

const contactName = ref('')
const contactEmail = ref('')
const contactPhone = ref(PHONE_PREFIX)
const contactConsent = ref(false)
const contactFormDismissed = ref(false)

const messagesEl = ref<HTMLElement | null>(null)
let pollTimer: ReturnType<typeof setInterval> | null = null

const isStaffRoute = () => route.path.startsWith('/staff')

const needsContactForm = computed(
  () =>
    !contactSubmitted.value &&
    (sessionStatus.value === 'waiting_manager' || sessionStatus.value === 'in_progress'),
)

const showContactForm = computed(() => needsContactForm.value)

const showContactFormCard = computed(
  () => showContactForm.value && !contactFormDismissed.value,
)

const showManagerButton = computed(
  () =>
    (sessionStatus.value === 'bot' || sessionStatus.value === 'closed') && !showContactForm.value,
)

const chatInputPlaceholder = computed(() => {
  if (sessionStatus.value === 'closed') return 'Чат закрыт'
  if (showContactFormCard.value) return 'Напишите сообщение менеджеру…'
  return 'Введите сообщение...'
})

const chatInputDisabled = computed(
  () => loading.value || sessionStatus.value === 'closed',
)

function closeContactForm() {
  contactFormDismissed.value = true
  contactError.value = ''
}

function openContactForm() {
  contactFormDismissed.value = false
  contactError.value = ''
  void scrollToBottom()
}

function phoneDigitsOnly(value: string): string {
  let digits = value.replace(/\D/g, '')
  if (digits.startsWith('8')) digits = '7' + digits.slice(1)
  if (digits.startsWith('7')) digits = digits.slice(1)
  return digits.slice(0, 10)
}

function formatPhoneSuffix(value: string): string {
  const d = phoneDigitsOnly(value)
  if (!d) return ''
  let out = d.slice(0, 3)
  if (d.length > 3) out += ` ${d.slice(3, 6)}`
  if (d.length > 6) out += `-${d.slice(6, 8)}`
  if (d.length > 8) out += `-${d.slice(8, 10)}`
  return out
}

const phoneDisplaySuffix = computed(() => formatPhoneSuffix(contactPhone.value))

function formatTime(iso: string) {
  return new Date(iso).toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' })
}

function isBotSide(sender: string) {
  return sender === 'bot' || sender === 'manager' || sender === 'system'
}

async function scrollToBottom() {
  await nextTick()
  const el = messagesEl.value
  if (el) el.scrollTop = el.scrollHeight
}

function applySession(data: ChatSessionPublic) {
  sessionKey.value = data.session_key
  sessionStatus.value = data.status
  messages.value = data.messages
  contactSubmitted.value = Boolean(data.contact_submitted)
  if (contactSubmitted.value || data.status !== 'waiting_manager') {
    contactFormDismissed.value = false
  }
  if (data.visitor_name) contactName.value = data.visitor_name
  if (data.email) contactEmail.value = data.email
  if (data.phone) contactPhone.value = data.phone
  localStorage.setItem(STORAGE_KEY, data.session_key)
}

async function ensureSession() {
  await initSession()
}

async function initSession() {
  const stored = localStorage.getItem(STORAGE_KEY) || ''
  const data = await apiFetch<ChatSessionPublic>('/chat/session/', {
    method: 'POST',
    body: JSON.stringify({
      session_key: stored || undefined,
      page_url: window.location.href,
    }),
  })
  applySession(data)
}

async function pollMessages() {
  if (!sessionKey.value || !isOpen.value) return
  try {
    const after = messages.value.at(-1)?.id ?? 0
    const data = await apiFetch<{
      status: ChatStatus
      messages: ChatMessage[]
      needs_contact_form: boolean
      contact_submitted: boolean
      visitor_name: string
      email: string
      phone: string
    }>(`/chat/session/${encodeURIComponent(sessionKey.value)}/messages/?after_id=${after}`)
    const prevStatus = sessionStatus.value
    sessionStatus.value = data.status
    contactSubmitted.value = Boolean(data.contact_submitted)
    if (
      data.needs_contact_form &&
      prevStatus === 'waiting_manager' &&
      data.status === 'in_progress'
    ) {
      contactFormDismissed.value = false
    }
    if (data.visitor_name) contactName.value = data.visitor_name
    if (data.email) contactEmail.value = data.email
    if (data.phone) contactPhone.value = data.phone
    if (data.messages.length) {
      messages.value = [...messages.value, ...data.messages]
      await scrollToBottom()
    }
  } catch {
    /* ignore */
  }
}

async function sendMessage() {
  const text = message.value.trim()
  if (!text || loading.value || sessionStatus.value === 'closed') return

  loading.value = true
  message.value = ''
  try {
    if (!sessionKey.value) await ensureSession()
    const data = await apiFetch<ChatSessionPublic>(
      `/chat/session/${encodeURIComponent(sessionKey.value)}/send/`,
      {
        method: 'POST',
        body: JSON.stringify({ text }),
      },
    )
    applySession(data)
    await scrollToBottom()
  } catch {
    message.value = text
  } finally {
    loading.value = false
  }
}

async function requestManager() {
  if (loading.value) return
  loading.value = true
  contactError.value = ''
  contactFormDismissed.value = false
  try {
    await ensureSession()
    const data = await apiFetch<ChatSessionPublic>(
      `/chat/session/${encodeURIComponent(sessionKey.value)}/escalate/`,
      { method: 'POST', body: JSON.stringify({}) },
    )
    applySession(data)
    if (!contactPhone.value.startsWith(PHONE_PREFIX)) {
      contactPhone.value = PHONE_PREFIX
    }
    await scrollToBottom()
  } catch (e) {
    contactError.value = e instanceof Error ? e.message : 'Не удалось вызвать менеджера'
  } finally {
    loading.value = false
  }
}

function normalizePhoneInput(raw: string): string {
  return PHONE_PREFIX + phoneDigitsOnly(raw)
}

function onPhonePartInput(event: Event) {
  const el = event.target as HTMLInputElement
  contactPhone.value = normalizePhoneInput(PHONE_PREFIX + el.value)
}

function onPhonePartKeydown(event: KeyboardEvent) {
  const el = event.target as HTMLInputElement
  if (el.value === '' && event.key === 'Backspace') {
    event.preventDefault()
  }
}

async function submitContact() {
  if (!sessionKey.value || loading.value) return
  if (!contactConsent.value) {
    contactError.value = 'Подтвердите согласие на обработку персональных данных'
    return
  }
  if (phoneDigitsOnly(contactPhone.value).length < 10) {
    contactError.value = 'Укажите номер телефона полностью'
    return
  }
  contactError.value = ''
  loading.value = true
  try {
    const data = await apiFetch<ChatSessionPublic>(
      `/chat/session/${encodeURIComponent(sessionKey.value)}/contact/`,
      {
        method: 'POST',
        body: JSON.stringify({
          name: contactName.value.trim(),
          email: contactEmail.value.trim(),
          phone: contactPhone.value,
        }),
      },
    )
    applySession(data)
    await scrollToBottom()
  } catch (e) {
    contactError.value = e instanceof Error ? e.message : 'Не удалось отправить'
  } finally {
    loading.value = false
  }
}

const toggleChat = async () => {
  isOpen.value = !isOpen.value
  if (isOpen.value) {
    try {
      await initSession()
      if (!contactPhone.value.startsWith(PHONE_PREFIX)) {
        contactPhone.value = PHONE_PREFIX
      }
      await scrollToBottom()
    } catch (e) {
      contactError.value = e instanceof Error ? e.message : 'Не удалось открыть чат'
    }
  }
}

function handleKeyPress(event: KeyboardEvent) {
  if (event.key === 'Enter') {
    void sendMessage()
  }
}

watch(isOpen, (open) => {
  if (open) {
    void pollMessages()
    if (!pollTimer) pollTimer = setInterval(() => void pollMessages(), 3000)
  }
})

watch(showContactFormCard, (show) => {
  if (show) void scrollToBottom()
})

onMounted(() => {
  if (!isStaffRoute()) {
    const stored = localStorage.getItem(STORAGE_KEY)
    if (stored) sessionKey.value = stored
  }
})

onUnmounted(() => {
  if (pollTimer) clearInterval(pollTimer)
})
</script>

<template>
  <div v-if="!isStaffRoute()" class="chatbot">
    <button class="chat-toggle" type="button" :class="{ open: isOpen }" @click="toggleChat">
      <svg v-if="!isOpen" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
      </svg>
      <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <line x1="18" y1="6" x2="6" y2="18" />
        <line x1="6" y1="6" x2="18" y2="18" />
      </svg>
    </button>

    <div class="chat-window" :class="{ open: isOpen, 'chat-window--contact': showContactFormCard }">
      <div class="chat-header" :class="{ 'chat-header--prompt': showContactForm || showContactFormCard }">
        <h3 v-if="showContactFormCard && sessionStatus === 'in_progress'">Менеджер на связи</h3>
        <h3 v-else-if="showContactFormCard">Отправьте нам сообщение</h3>
        <h3 v-else-if="showContactForm">Ожидаем менеджера</h3>
        <h3 v-else>Техническая поддержка</h3>
        <p v-if="showContactFormCard && sessionStatus === 'in_progress'">
          Укажите контакты, чтобы мы могли связаться с вами
        </p>
        <p v-else-if="sessionStatus === 'in_progress'">Менеджер на связи</p>
        <p v-else-if="!showContactFormCard">Онлайн</p>
      </div>

      <div class="chat-body">
        <div ref="messagesEl" class="chat-messages">
        <div
          v-for="msg in messages"
          :key="msg.id"
          class="message"
          :class="{ 'message-bot': isBotSide(msg.sender_type), 'message-user': msg.sender_type === 'visitor' }"
        >
          <div class="message-content">
            <p class="message-text">{{ msg.text }}</p>
            <span class="message-time">{{ formatTime(msg.created_at) }}</span>
          </div>
        </div>
        </div>

        <div v-if="needsContactForm && contactFormDismissed" class="chat-contact-reopen">
          <button type="button" class="chat-contact-reopen-btn" @click="openContactForm">
            Указать контакты
          </button>
        </div>

        <div v-if="showContactFormCard" class="chat-contact-wrap">
          <p class="chat-contact-hint">
            Укажите контакты или напишите сообщение ниже — менеджер увидит переписку
          </p>

          <form class="chat-contact-card" @submit.prevent="submitContact">
            <button
              type="button"
              class="chat-contact-collapse"
              aria-label="Свернуть форму"
              @click="closeContactForm"
            >
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="6 9 12 15 18 9" />
              </svg>
            </button>

            <label class="chat-field-underline">
            <input
              v-model="contactName"
              type="text"
              required
              autocomplete="name"
              placeholder="Ваше имя*"
            />
          </label>

          <label class="chat-field-underline">
            <input
              v-model="contactEmail"
              type="email"
              required
              autocomplete="email"
              placeholder="Ваш e-mail*"
            />
          </label>

          <div class="chat-phone-block">
            <span class="chat-phone-label">Ваш телефон</span>
            <div class="chat-phone-row">
              <span class="chat-phone-country" title="Россия">
                <span class="chat-phone-flag" aria-hidden="true">🇷🇺</span>
                <span class="chat-phone-code">{{ PHONE_PREFIX }}</span>
              </span>
              <input
                :value="phoneDisplaySuffix"
                type="tel"
                inputmode="numeric"
                autocomplete="tel-national"
                class="chat-phone-input"
                placeholder="000 000-00-00"
                required
                @input="onPhonePartInput"
                @keydown="onPhonePartKeydown"
              />
            </div>
          </div>

          <label class="chat-consent">
            <input v-model="contactConsent" type="checkbox" />
            <span>
              Я даю
              <strong>согласие</strong>
              на обработку персональных данных*
            </span>
          </label>

          <p v-if="contactError" class="chat-contact-error">{{ contactError }}</p>

            <button type="submit" class="chat-contact-submit" :disabled="loading">
              {{ loading ? 'Отправка…' : 'Отправить' }}
            </button>
          </form>
        </div>
      </div>

      <div v-if="showManagerButton" class="chat-quick-actions">
        <button type="button" class="chat-quick-btn" :disabled="loading" @click="requestManager">
          Менеджер
        </button>
      </div>

      <p v-if="contactError && !showContactForm" class="chat-global-error">{{ contactError }}</p>

      <div class="chat-input">
        <input
          v-model="message"
          type="text"
          :placeholder="chatInputPlaceholder"
          :disabled="chatInputDisabled"
          @keypress="handleKeyPress"
        />
        <button
          type="button"
          class="send-btn"
          :disabled="loading || chatInputDisabled || !message.trim()"
          @click="sendMessage"
        >
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="22" y1="2" x2="11" y2="13" />
            <polygon points="22 2 15 22 11 13 2 9 22 2" />
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.chatbot {
  position: fixed;
  bottom: 30px;
  right: 30px;
  z-index: 1000;
}

.chat-toggle {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: #ff7722;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 15px rgba(255, 119, 34, 0.4);
  transition: all 0.3s;
}

.chat-toggle:hover {
  background: #e66611;
  transform: scale(1.1);
}

.chat-toggle svg {
  width: 28px;
  height: 28px;
  color: white;
}

.chat-window {
  position: absolute;
  bottom: 80px;
  right: 0;
  width: 350px;
  height: 520px;
  background: #f3f3f3;
  border-radius: 20px;
  box-shadow: 0 5px 30px rgba(0, 0, 0, 0.2);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  opacity: 0;
  visibility: hidden;
  transform: translateY(20px);
  transition: all 0.3s;
}

.chat-window--contact {
  height: 560px;
}

.chat-window.open {
  opacity: 1;
  visibility: visible;
  transform: translateY(0);
}

.chat-header {
  background: #ff7722;
  color: white;
  padding: 18px 20px 22px;
  text-align: center;
  flex-shrink: 0;
  position: relative;
  z-index: 1;
}

.chat-header--prompt {
  padding-bottom: 24px;
  background: linear-gradient(145deg, #ff8833 0%, #ff7722 45%, #e86a18 100%);
}

.chat-header h3 {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 5px;
  font-family: var(--font-heading);
}

.chat-header p {
  font-size: 13px;
  opacity: 0.9;
}

.chat-body {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 0;
  overflow-y: auto;
}

.chat-messages {
  flex: 0 0 auto;
  padding: 12px 14px 8px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.chat-window--contact .chat-messages {
  max-height: 42%;
  overflow-y: auto;
  flex-shrink: 0;
}

.chat-global-error {
  margin: 0;
  padding: 8px 14px;
  font-size: 12px;
  color: #c62828;
  background: #fff;
  border-top: 1px solid #fdecea;
}

.message {
  display: flex;
  max-width: 85%;
}

.message-bot {
  align-self: flex-start;
}

.message-user {
  align-self: flex-end;
  justify-content: flex-end;
}

.message-content {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.message-text {
  padding: 12px 16px;
  border-radius: 15px;
  font-size: 14px;
  line-height: 1.5;
  white-space: pre-wrap;
}

.message-bot .message-text {
  background: #e8e8e8;
  color: #333;
  border-bottom-left-radius: 5px;
}

.message-user .message-text {
  background: #ff7722;
  color: white;
  border-bottom-right-radius: 5px;
}

.message-time {
  font-size: 11px;
  color: #999;
  padding: 0 5px;
}

.chat-contact-reopen {
  flex-shrink: 0;
  padding: 8px 12px 0;
  background: #fff;
}

.chat-contact-reopen-btn {
  width: 100%;
  padding: 10px 14px;
  border: 1px dashed #ff7722;
  border-radius: 10px;
  background: #fff8f3;
  color: #e66611;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}

.chat-contact-reopen-btn:hover {
  background: #ffefe4;
}

.chat-contact-wrap {
  flex-shrink: 0;
  padding: 8px 12px 10px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.chat-contact-hint {
  margin: 0;
  padding: 0 8px;
  text-align: center;
  font-size: 13px;
  line-height: 1.45;
  color: #777;
}

.chat-contact-card {
  margin: 0;
  padding: 16px 40px 16px 16px;
  background: #fff;
  border-radius: 12px;
  border-top: 3px solid #ff7722;
  box-shadow: 0 2px 16px rgba(0, 0, 0, 0.08);
  display: flex;
  flex-direction: column;
  gap: 14px;
  position: relative;
}

.chat-contact-collapse {
  position: absolute;
  top: 50%;
  right: -14px;
  transform: translateY(-50%);
  width: 32px;
  height: 32px;
  padding: 0;
  border: none;
  border-radius: 50%;
  background: #fff;
  color: #666;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.12);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.2s, color 0.2s;
}

.chat-contact-collapse:hover {
  background: #fafafa;
  color: #333;
}

.chat-contact-collapse svg {
  width: 18px;
  height: 18px;
}

.chat-field-underline input {
  width: 100%;
  padding: 8px 0 10px;
  border: none;
  border-bottom: 1px solid #d8d8d8;
  border-radius: 0;
  font-size: 15px;
  outline: none;
  background: transparent;
  transition: border-color 0.2s;
}

.chat-field-underline input::placeholder {
  color: #aaa;
}

.chat-field-underline input:focus {
  border-bottom-color: #ff7722;
}

.chat-phone-block {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.chat-phone-label {
  font-size: 12px;
  color: #888;
}

.chat-phone-row {
  display: flex;
  align-items: center;
  gap: 8px;
  border-bottom: 1px solid #d8d8d8;
  padding-bottom: 8px;
}

.chat-phone-country {
  display: flex;
  align-items: center;
  gap: 4px;
  flex-shrink: 0;
  padding-right: 8px;
  border-right: 1px solid #e8e8e8;
}

.chat-phone-flag {
  font-size: 18px;
  line-height: 1;
}

.chat-phone-code {
  font-size: 15px;
  font-weight: 500;
  color: #333;
}

.chat-phone-input {
  flex: 1;
  min-width: 0;
  border: none;
  outline: none;
  font-size: 15px;
  background: transparent;
  letter-spacing: 0.02em;
}

.chat-phone-input::placeholder {
  color: #bbb;
}

.chat-consent {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  font-size: 11px;
  line-height: 1.45;
  color: #666;
  cursor: pointer;
}

.chat-consent input {
  margin-top: 2px;
  flex-shrink: 0;
  accent-color: #ff7722;
}

.chat-consent strong {
  color: #1a73e8;
  font-weight: 600;
}

.chat-contact-error {
  margin: 0;
  font-size: 12px;
  color: #c62828;
}

.chat-contact-submit {
  width: 100%;
  padding: 12px 16px;
  background: #ff7722;
  color: #fff;
  border: none;
  border-radius: 12px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}

.chat-contact-submit:hover:not(:disabled) {
  background: #e66611;
}

.chat-contact-submit:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.chat-quick-actions {
  display: flex;
  gap: 8px;
  padding: 8px 15px 0;
  background: #fff;
  flex-shrink: 0;
}

.chat-quick-btn {
  padding: 6px 12px;
  font-size: 12px;
  border: 1px solid #ff7722;
  color: #ff7722;
  background: #fff;
  border-radius: 16px;
  cursor: pointer;
}

.chat-quick-btn:hover:not(:disabled) {
  background: #fff5ee;
}

.chat-quick-btn:disabled {
  opacity: 0.5;
}

.chat-input {
  display: flex;
  gap: 10px;
  padding: 15px;
  background: white;
  border-top: 1px solid #e8e8e8;
  flex-shrink: 0;
}

.chat-input input {
  flex: 1;
  padding: 12px 15px;
  border: 1px solid #e8e8e8;
  border-radius: 25px;
  font-size: 14px;
  outline: none;
  transition: border-color 0.3s;
}

.chat-input input:focus {
  border-color: #ff7722;
}

.send-btn {
  width: 45px;
  height: 45px;
  border-radius: 50%;
  background: #ff7722;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
}

.send-btn:hover:not(:disabled) {
  background: #e66611;
  transform: scale(1.05);
}

.send-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.send-btn svg {
  width: 20px;
  height: 20px;
  color: white;
}

@media (max-width: 640px) {
  .chatbot {
    bottom: 20px;
    right: 20px;
  }

  .chat-window {
    width: 300px;
    height: 460px;
    bottom: 70px;
  }

  .chat-toggle {
    width: 55px;
    height: 55px;
  }
}
</style>
