<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useStaffQuoteNotifications } from '@/composables/useStaffQuoteNotifications'

const router = useRouter()
const { newCount, preview, markSeen } = useStaffQuoteNotifications()

function openInbox() {
  markSeen()
  if (router.currentRoute.value.path !== '/staff/inbox') {
    router.push('/staff/inbox')
  }
}

function dismiss() {
  markSeen()
}
</script>

<template>
  <div v-if="newCount > 0" class="staff-notify" role="status">
    <p class="staff-notify-title">
      {{ newCount === 1 ? 'Новая заявка' : `Новых заявок: ${newCount}` }}
    </p>
    <ul v-if="preview.length" class="staff-notify-list">
      <li v-for="item in preview" :key="`${item.request_type}-${item.public_number}`">
        <span class="staff-notify-type">{{ item.type_label }}</span>
        <strong>{{ item.title }}</strong>
        <span v-if="item.request_type === 'quote' && item.has_attachments" class="staff-notify-badge">
          макет
        </span>
      </li>
    </ul>
    <div class="staff-notify-actions">
      <button type="button" class="staff-notify-btn" @click="openInbox">Открыть заявки</button>
      <button type="button" class="staff-notify-dismiss" @click="dismiss">Скрыть</button>
    </div>
  </div>
</template>

<style scoped>
.staff-notify {
  margin-bottom: 16px;
  padding: 12px 16px;
  background: #fff8f0;
  border: 1px solid #ffc89a;
  border-radius: 8px;
}
.staff-notify-title {
  margin: 0 0 8px;
  font-weight: 600;
  color: #c45a00;
}
.staff-notify-list {
  margin: 0 0 10px;
  padding-left: 18px;
  font-size: 0.9rem;
  color: #444;
}
.staff-notify-type {
  display: inline-block;
  margin-right: 6px;
  font-size: 0.75rem;
  color: #888;
}
.staff-notify-badge {
  margin-left: 8px;
  font-size: 0.75rem;
  color: #666;
}
.staff-notify-actions {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}
.staff-notify-btn {
  padding: 6px 14px;
  background: #ff7722;
  color: #fff;
  border: none;
  border-radius: 6px;
  font-size: 0.85rem;
  cursor: pointer;
}
.staff-notify-dismiss {
  padding: 6px 14px;
  background: transparent;
  color: #666;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 0.85rem;
  cursor: pointer;
}
</style>
