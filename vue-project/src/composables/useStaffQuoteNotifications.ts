import { onMounted, onUnmounted, ref } from 'vue'
import { apiFetch } from '@/api/http'
import type { InboxListItem } from '@/types/inbox'

const STORAGE_KEY = 'staff_inbox_last_seen_at'
const POLL_MS = 45_000

const newCount = ref(0)
const preview = ref<InboxListItem[]>([])

let pollTimer: ReturnType<typeof setInterval> | null = null
let subscribers = 0

function getLastSeenMs(): number {
  const raw = localStorage.getItem(STORAGE_KEY)
  if (!raw) {
    const now = Date.now()
    localStorage.setItem(STORAGE_KEY, new Date(now).toISOString())
    return now
  }
  const ms = Date.parse(raw)
  return Number.isNaN(ms) ? Date.now() : ms
}

export function markStaffQuotesSeen() {
  localStorage.setItem(STORAGE_KEY, new Date().toISOString())
  newCount.value = 0
  preview.value = []
}

export async function refreshStaffQuoteNotifications() {
  try {
    const items = await apiFetch<InboxListItem[]>('/staff/inbox/')
    const seenAt = getLastSeenMs()
    const unseen = items.filter((row) => Date.parse(row.created_at) > seenAt)
    newCount.value = unseen.length
    preview.value = unseen.slice(0, 5)
  } catch {
    newCount.value = 0
    preview.value = []
  }
}

function startPolling() {
  if (pollTimer) return
  void refreshStaffQuoteNotifications()
  pollTimer = setInterval(() => void refreshStaffQuoteNotifications(), POLL_MS)
}

function stopPolling() {
  if (pollTimer) {
    clearInterval(pollTimer)
    pollTimer = null
  }
}

/** Уведомления о новых заявках (расчёт и звонок) для раздела staff. */
export function useStaffQuoteNotifications() {
  onMounted(() => {
    subscribers += 1
    if (subscribers === 1) startPolling()
  })

  onUnmounted(() => {
    subscribers -= 1
    if (subscribers === 0) stopPolling()
  })

  return {
    newCount,
    preview,
    markSeen: markStaffQuotesSeen,
    refresh: refreshStaffQuoteNotifications,
  }
}
