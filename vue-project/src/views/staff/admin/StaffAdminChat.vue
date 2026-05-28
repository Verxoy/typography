<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue'
import { apiFetch } from '@/api/http'
import StaffAdminShell from '@/components/staff/StaffAdminShell.vue'

type FaqRule = {
  id: number
  pattern: string
  reply: string
  priority: number
  is_active: boolean
}

const faq = ref<FaqRule[]>([])
const keywordsText = ref('')
const message = ref('')

const templateKeys = [
  'welcome',
  'default_reply',
  'escalate_prompt',
  'escalate_confirm',
  'contact_thanks',
  'manager_joined',
] as const

const templateTexts = reactive<Record<string, string>>({})

const newRule = ref({ pattern: '', reply: '', priority: 0 })

async function load() {
  faq.value = await apiFetch<FaqRule[]>('/staff/cms/chat/faq/')
  const templates = await apiFetch<{ key: string; text: string }[]>('/staff/cms/chat/templates/')
  for (const key of templateKeys) {
    templateTexts[key] = templates.find((t) => t.key === key)?.text ?? ''
  }
  const kws = await apiFetch<{ keyword: string }[]>('/staff/cms/chat/keywords/')
  keywordsText.value = kws.map((k) => k.keyword).join('\n')
}

async function addRule() {
  await apiFetch('/staff/cms/chat/faq/', {
    method: 'POST',
    body: JSON.stringify(newRule.value),
  })
  newRule.value = { pattern: '', reply: '', priority: 0 }
  await load()
  message.value = 'Правило добавлено'
}

async function saveRule(r: FaqRule) {
  await apiFetch(`/staff/cms/chat/faq/${r.id}/`, {
    method: 'PATCH',
    body: JSON.stringify(r),
  })
  message.value = 'Сохранено'
}

async function deleteRule(id: number) {
  if (!confirm('Удалить правило?')) return
  await apiFetch(`/staff/cms/chat/faq/${id}/`, { method: 'DELETE' })
  await load()
}

async function saveTemplates() {
  await apiFetch('/staff/cms/chat/templates/', {
    method: 'PUT',
    body: JSON.stringify({
      templates: templateKeys.map((key) => ({ key, text: templateTexts[key] ?? '' })),
    }),
  })
  message.value = 'Шаблоны сохранены'
}

async function saveKeywords() {
  const keywords = keywordsText.value
    .split(/[\n,]+/)
    .map((s) => s.trim())
    .filter(Boolean)
  await apiFetch('/staff/cms/chat/keywords/', {
    method: 'PUT',
    body: JSON.stringify({ keywords }),
  })
  message.value = 'Ключевые слова сохранены'
}

onMounted(() => void load())
</script>

<template>
  <StaffAdminShell>
    <h2 class="admin-h2">Чат-бот</h2>
    <p v-if="message" class="admin-ok">{{ message }}</p>

    <section class="admin-card">
      <h3>Правила FAQ</h3>
      <div class="admin-table-wrap">
        <table class="admin-table">
          <thead>
            <tr>
              <th>Паттерн</th>
              <th>Ответ</th>
              <th>Приоритет</th>
              <th>Активно</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="r in faq" :key="r.id">
              <td><input v-model="r.pattern" class="admin-inp" /></td>
              <td><textarea v-model="r.reply" class="admin-inp" rows="2" /></td>
              <td><input v-model.number="r.priority" type="number" class="admin-inp admin-inp--xs" /></td>
              <td><input v-model="r.is_active" type="checkbox" /></td>
              <td>
                <button type="button" class="admin-btn-sm" @click="saveRule(r)">OK</button>
                <button type="button" class="admin-btn-sm admin-btn-sm--danger" @click="deleteRule(r.id)">×</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <h4 class="admin-h4">Новое правило</h4>
      <input v-model="newRule.pattern" class="admin-inp" placeholder="Паттерн (regex)" />
      <textarea v-model="newRule.reply" class="admin-inp" rows="2" placeholder="Ответ" />
      <button type="button" class="admin-btn" @click="addRule">Добавить</button>
    </section>

    <section class="admin-card">
      <h3>Системные сообщения</h3>
      <div v-for="key in templateKeys" :key="key" class="tpl-row">
        <label class="admin-label">{{ key }}</label>
        <textarea v-model="templateTexts[key]" class="admin-inp" rows="2" />
      </div>
      <button type="button" class="admin-btn" @click="saveTemplates">Сохранить шаблоны</button>
    </section>

    <section class="admin-card">
      <h3>Слова для передачи менеджеру</h3>
      <textarea v-model="keywordsText" class="admin-textarea" rows="6" />
      <button type="button" class="admin-btn" @click="saveKeywords">Сохранить</button>
    </section>
  </StaffAdminShell>
</template>

<style scoped>
@import './admin-shared.css';
.tpl-row {
  margin-bottom: 12px;
}
.admin-label {
  display: block;
  font-size: 0.85rem;
  font-weight: 600;
  margin-bottom: 4px;
}
.admin-btn-sm--danger {
  background: #a33;
  margin-left: 4px;
}
</style>
