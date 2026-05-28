<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue'
import RuPhoneInput from '@/components/RuPhoneInput.vue'
import { apiFetch, apiFetchFormData } from '@/api/http'
import { isRuPhoneComplete, ruPhoneForApi } from '@/utils/ruPhone'
import type { QuoteService } from '@/types/quotes'

const step = ref(1)
const loading = ref(false)
const error = ref('')
const services = ref<QuoteService[]>([])
const selectedSlug = ref('')
const parameters = reactive<Record<string, string>>({})
const layoutFiles = ref<File[]>([])
const layoutPreviews = ref<{ name: string; url: string }[]>([])

const orderAsCompany = ref(false)

const contacts = reactive({
  company_type: 'ooo' as 'ip' | 'ooo' | 'private',
  company_name: '',
  inn: '',
  contact_name: '',
  contact_phone: '',
  contact_email: '',
  client_comment: '',
})

const selectedService = computed(() =>
  services.value.find((s) => s.slug === selectedSlug.value),
)

onMounted(async () => {
  try {
    const data = await apiFetch<{ services: QuoteService[] }>('/quotes/catalog/')
    services.value = data.services
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Не удалось загрузить услуги'
  }
})

function selectService(slug: string) {
  selectedSlug.value = slug
  const svc = services.value.find((s) => s.slug === slug)
  Object.keys(parameters).forEach((k) => delete parameters[k])
  if (svc) {
    for (const f of svc.fields) {
      parameters[f.key] = ''
    }
  }
}

function nextStep() {
  error.value = ''
  if (step.value === 1 && !selectedSlug.value) {
    error.value = 'Выберите тип заказа'
    return
  }
  if (step.value === 2) {
    const svc = selectedService.value
    if (!svc) return
    for (const f of svc.fields) {
      if (f.required && !parameters[f.key]?.trim()) {
        error.value = `Заполните поле «${f.label}»`
        return
      }
    }
  }
  step.value += 1
}

function prevStep() {
  error.value = ''
  if (step.value > 1) step.value -= 1
}

function validateInn(): string | null {
  const digits = contacts.inn.replace(/\D/g, '')
  if (contacts.company_type === 'ooo' && digits.length !== 10) {
    return 'Для ООО ИНН должен содержать 10 цифр.'
  }
  if (contacts.company_type === 'ip' && digits.length !== 12) {
    return 'Для ИП ИНН должен содержать 12 цифр.'
  }
  contacts.inn = digits
  return null
}

const ALLOWED_LAYOUT_EXT = /\.(jpe?g|png|gif|webp|pdf|ai|eps|cdr|zip|rar)$/i
const MAX_LAYOUT_FILES = 3
const MAX_LAYOUT_BYTES = 25 * 1024 * 1024

function revokeLayoutPreviews() {
  layoutPreviews.value.forEach((p) => URL.revokeObjectURL(p.url))
  layoutPreviews.value = []
}

function onLayoutFilesChange(event: Event) {
  error.value = ''
  const input = event.target as HTMLInputElement
  const picked = Array.from(input.files || [])
  input.value = ''

  const combined = [...layoutFiles.value, ...picked].slice(0, MAX_LAYOUT_FILES)
  for (const file of combined) {
    if (!ALLOWED_LAYOUT_EXT.test(file.name)) {
      error.value = 'Допустимы: JPG, PNG, PDF, AI, EPS, CDR, ZIP, RAR'
      return
    }
    if (file.size > MAX_LAYOUT_BYTES) {
      error.value = 'Размер одного файла — не более 25 МБ'
      return
    }
  }

  revokeLayoutPreviews()
  layoutFiles.value = combined
  layoutPreviews.value = combined
    .filter((f) => /^image\//i.test(f.type) || /\.(jpe?g|png|gif|webp)$/i.test(f.name))
    .map((f) => ({ name: f.name, url: URL.createObjectURL(f) }))
}

function removeLayoutFile(index: number) {
  revokeLayoutPreviews()
  layoutFiles.value = layoutFiles.value.filter((_, i) => i !== index)
  layoutPreviews.value = layoutFiles.value
    .filter((f) => /^image\//i.test(f.type) || /\.(jpe?g|png|gif|webp)$/i.test(f.name))
    .map((f) => ({ name: f.name, url: URL.createObjectURL(f) }))
}

async function submit() {
  error.value = ''
  if (!contacts.contact_name.trim() || !contacts.contact_phone.trim() || !contacts.contact_email.trim()) {
    error.value = 'Укажите, как с вами связаться: имя, телефон и email'
    return
  }
  if (!isRuPhoneComplete(contacts.contact_phone)) {
    error.value = 'Укажите полный номер телефона в формате +7 (999) 999-99-99'
    return
  }

  if (orderAsCompany.value) {
    contacts.company_type = contacts.company_type === 'ip' ? 'ip' : 'ooo'
    if (!contacts.company_name.trim()) {
      error.value = 'Укажите название организации'
      return
    }
    if (!contacts.inn.trim()) {
      error.value = 'Укажите ИНН или снимите галочку «Заказ от организации»'
      return
    }
    const innError = validateInn()
    if (innError) {
      error.value = innError
      return
    }
  } else {
    contacts.company_type = 'private'
    contacts.company_name = ''
    contacts.inn = ''
  }

  const formData = new FormData()
  formData.append('service_slug', selectedSlug.value)
  formData.append('parameters', JSON.stringify({ ...parameters }))
  formData.append('company_type', contacts.company_type)
  formData.append('company_name', contacts.company_name.trim())
  formData.append('inn', contacts.inn)
  formData.append('contact_name', contacts.contact_name.trim())
  formData.append('contact_phone', ruPhoneForApi(contacts.contact_phone))
  formData.append('contact_email', contacts.contact_email.trim())
  formData.append('client_comment', contacts.client_comment.trim())
  for (const file of layoutFiles.value) {
    formData.append('layout_files', file)
  }

  loading.value = true
  try {
    await apiFetchFormData('/quotes/submit/', formData, {
      method: 'POST',
    })
    revokeLayoutPreviews()
    layoutFiles.value = []
    step.value = 4
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Не удалось отправить заявку'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="app">
    <main class="main-content">
      <div class="container">
        <router-link to="/" class="page-back-link">← На главную</router-link>

        <h1 class="page-title">Быстрый расчёт</h1>
        <p class="page-subtitle">
          Не нужно знать все параметры заранее — опишите задачу своими словами.
          Мы подготовим коммерческое предложение с точной стоимостью и свяжемся с вами.
        </p>

        <div v-if="step < 4" class="quote-steps">
          <span :class="{ active: step >= 1 }">1. Тип заказа</span>
          <span :class="{ active: step >= 2 }">2. О заказе</span>
          <span :class="{ active: step >= 3 }">3. Связь с вами</span>
        </div>

        <p v-if="error" class="quote-error">{{ error }}</p>

        <!-- Шаг 1 -->
        <section v-if="step === 1" class="form-block">
          <h2 class="form-block-title">Что ближе к вашей задаче?</h2>
          <p class="form-block-hint form-block-hint--top">
            Выберите вариант — на следующем шаге достаточно коротко описать заказ.
          </p>
          <div class="quote-services">
            <button
              v-for="svc in services"
              :key="svc.slug"
              type="button"
              class="quote-service-card"
              :class="{ selected: selectedSlug === svc.slug }"
              @click="selectService(svc.slug)"
            >
              <h3>{{ svc.title }}</h3>
              <p>{{ svc.hint }}</p>
            </button>
          </div>
          <div class="form-actions">
            <button type="button" class="submit-button" @click="nextStep">Далее</button>
          </div>
        </section>

        <!-- Шаг 2 -->
        <section v-else-if="step === 2 && selectedService" class="form-block">
          <h2 class="form-block-title">{{ selectedService.title }}</h2>
          <p class="form-block-hint">{{ selectedService.hint }}</p>
          <p class="quote-step-note">
            Обязательно только поле «Что нужно сделать» — остальное можно пропустить или выбрать «Пока не знаю».
          </p>
          <form class="quote-form" @submit.prevent="nextStep">
            <div
              v-for="field in selectedService.fields"
              :key="field.key"
              class="form-group"
            >
              <label class="form-label">
                {{ field.label }}<template v-if="field.required"> *</template>
              </label>
              <select
                v-if="field.type === 'select'"
                v-model="parameters[field.key]"
                class="form-select"
                :required="field.required"
              >
                <option value="">— выберите —</option>
                <option v-for="opt in field.options" :key="opt" :value="opt">{{ opt }}</option>
              </select>
              <textarea
                v-else-if="field.type === 'textarea'"
                v-model="parameters[field.key]"
                class="form-textarea"
                rows="4"
                :placeholder="field.placeholder"
                :required="field.required"
              />
              <input
                v-else
                v-model="parameters[field.key]"
                type="text"
                class="form-input"
                :placeholder="field.placeholder"
                :required="field.required"
              />
            </div>
            <div class="form-actions">
              <button type="button" class="submit-button submit-button--secondary" @click="prevStep">
                Назад
              </button>
              <button type="submit" class="submit-button">Далее</button>
            </div>
          </form>
        </section>

        <!-- Шаг 3 -->
        <section v-else-if="step === 3" class="form-block">
          <h2 class="form-block-title">Как с вами связаться</h2>
          <p class="form-block-hint">Контакты обязательны. Реквизиты организации — только если нужен счёт на юрлицо.</p>
          <form class="quote-form" @submit.prevent="submit">
            <div class="form-group">
              <label class="form-label">Контактное лицо *</label>
              <input v-model="contacts.contact_name" type="text" class="form-input" required />
            </div>
            <div class="form-group">
              <label class="form-label">Телефон *</label>
              <RuPhoneInput v-model="contacts.contact_phone" required />
            </div>
            <div class="form-group">
              <label class="form-label">Email *</label>
              <input v-model="contacts.contact_email" type="email" class="form-input" required />
            </div>

            <label class="quote-company-toggle">
              <input v-model="orderAsCompany" type="checkbox" />
              <span>Заказ от организации (нужен счёт на ООО или ИП)</span>
            </label>

            <template v-if="orderAsCompany">
              <div class="form-group">
                <span class="form-label">Тип организации *</span>
                <div class="quote-radio-row">
                  <label><input v-model="contacts.company_type" type="radio" value="ooo" /> ООО</label>
                  <label><input v-model="contacts.company_type" type="radio" value="ip" /> ИП</label>
                </div>
              </div>
              <div class="form-group">
                <label class="form-label">Название организации *</label>
                <input v-model="contacts.company_name" type="text" class="form-input" />
              </div>
              <div class="form-group">
                <label class="form-label">ИНН *</label>
                <input
                  v-model="contacts.inn"
                  type="text"
                  class="form-input"
                  inputmode="numeric"
                  :maxlength="contacts.company_type === 'ip' ? 12 : 10"
                  :placeholder="contacts.company_type === 'ip' ? '12 цифр' : '10 цифр'"
                />
                <small class="field-hint">
                  {{ contacts.company_type === 'ip' ? 'ИП — 12 цифр' : 'ООО — 10 цифр' }}
                </small>
              </div>
            </template>

            <div class="form-group">
              <label class="form-label">Макет (необязательно)</label>
              <p class="field-hint">До {{ MAX_LAYOUT_FILES }} файлов, до 25 МБ каждый: JPG, PNG, PDF, AI, EPS, CDR, ZIP</p>
              <input
                type="file"
                class="quote-file-input"
                multiple
                accept=".jpg,.jpeg,.png,.gif,.webp,.pdf,.ai,.eps,.cdr,.zip,.rar,image/*"
                @change="onLayoutFilesChange"
              />
              <ul v-if="layoutFiles.length" class="quote-file-list">
                <li v-for="(file, idx) in layoutFiles" :key="file.name + idx" class="quote-file-item">
                  <span class="quote-file-name">{{ file.name }}</span>
                  <button type="button" class="quote-file-remove" @click="removeLayoutFile(idx)">
                    Удалить
                  </button>
                </li>
              </ul>
              <div v-if="layoutPreviews.length" class="quote-file-previews">
                <figure v-for="prev in layoutPreviews" :key="prev.url" class="quote-file-preview">
                  <img :src="prev.url" :alt="prev.name" />
                  <figcaption>{{ prev.name }}</figcaption>
                </figure>
              </div>
            </div>

            <div class="form-group">
              <label class="form-label">Дополнительно (необязательно)</label>
              <textarea
                v-model="contacts.client_comment"
                class="form-textarea"
                rows="3"
                placeholder="Удобное время для звонка, пожелания…"
              />
            </div>
            <p class="quote-disclaimer">
              Нажимая «Отправить», вы соглашаетесь на обработку данных для подготовки коммерческого предложения.
              Итоговая стоимость будет указана в коммерческом предложении.
            </p>
            <div class="form-actions">
              <button type="button" class="submit-button submit-button--secondary" @click="prevStep">
                Назад
              </button>
              <button type="submit" class="submit-button" :disabled="loading">
                {{ loading ? 'Отправка…' : 'Отправить' }}
              </button>
            </div>
          </form>
        </section>

        <!-- Успех -->
        <section v-else-if="step === 4" class="form-block quote-success">
          <div class="quote-success-icon">✓</div>
          <h2 class="form-block-title">Заявка принята</h2>
          <p class="quote-success-text">
            Точную стоимость рассчитаем и пришлём в коммерческом предложении.
            Менеджер свяжется с вами — отслеживание на сайте не требуется.
          </p>
          <router-link to="/" class="submit-button">На главную</router-link>
        </section>
      </div>
    </main>
  </div>
</template>

<style scoped>
.quote-steps {
  display: flex;
  justify-content: center;
  gap: 12px;
  margin-bottom: 30px;
  flex-wrap: wrap;
}

.quote-steps span {
  padding: 8px 18px;
  border-radius: 25px;
  background: #e8e8e8;
  color: #666;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.3s;
}

.quote-steps span.active {
  background: #ff7722;
  color: #fff;
}

.form-block-title {
  font-size: 28px;
  color: #333;
  margin-bottom: 10px;
  font-family: var(--font-heading);
}

.form-block-hint {
  font-size: 15px;
  color: #666;
  margin-bottom: 24px;
}

.form-block-hint--top {
  margin-top: -4px;
}

.quote-step-note {
  margin: -12px 0 20px;
  padding: 12px 16px;
  border-radius: 12px;
  background: rgba(255, 119, 34, 0.08);
  border: 1px solid rgba(255, 119, 34, 0.2);
  font-size: 14px;
  color: #555;
  line-height: 1.5;
}

.quote-company-toggle {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding: 14px 16px;
  border-radius: 12px;
  background: #f8f8f8;
  border: 1px solid #e8e8e8;
  cursor: pointer;
  font-size: 15px;
  color: #333;
  line-height: 1.45;
}

.quote-company-toggle input {
  margin-top: 3px;
  flex-shrink: 0;
}

.quote-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.quote-services {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-bottom: 24px;
}

.quote-service-card {
  text-align: left;
  padding: 20px 24px;
  border: 2px solid #e8e8e8;
  border-radius: 15px;
  background: white;
  cursor: pointer;
  transition: all 0.3s;
}

.quote-service-card:hover {
  border-color: #ff9955;
  transform: translateX(4px);
}

.quote-service-card.selected {
  border-color: #ff7722;
  border-left-width: 4px;
  box-shadow: 0 4px 12px rgba(255, 119, 34, 0.15);
}

.quote-service-card h3 {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 8px;
  color: #333;
  font-family: var(--font-heading);
}

.quote-service-card p {
  font-size: 15px;
  color: #666;
  margin: 0;
  line-height: 1.5;
}

.quote-radio-row {
  display: flex;
  gap: 24px;
  padding-top: 4px;
}

.quote-radio-row label {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  font-size: 15px;
  color: #333;
}

.field-hint {
  font-size: 13px;
  color: #888;
}

.quote-disclaimer {
  font-size: 14px;
  color: #666;
  line-height: 1.6;
}

.quote-error {
  color: #c0392b;
  margin-bottom: 20px;
  padding: 12px 16px;
  background: #fdecea;
  border-radius: 12px;
  font-size: 14px;
  max-width: 800px;
  margin-left: auto;
  margin-right: auto;
}

.quote-success {
  text-align: center;
}

.quote-success-icon {
  width: 72px;
  height: 72px;
  margin: 0 auto 20px;
  border-radius: 50%;
  background: #00aa44;
  color: #fff;
  font-size: 2rem;
  line-height: 72px;
}

.quote-success-text {
  color: #666;
  line-height: 1.6;
  margin-bottom: 28px;
  max-width: 520px;
  margin-left: auto;
  margin-right: auto;
}

.quote-file-input {
  display: block;
  width: 100%;
  font-size: 14px;
  margin-top: 6px;
}

.quote-file-list {
  list-style: none;
  margin: 12px 0 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.quote-file-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 8px 12px;
  background: #f5f5f5;
  border-radius: 10px;
  font-size: 14px;
}

.quote-file-name {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.quote-file-remove {
  flex-shrink: 0;
  border: none;
  background: transparent;
  color: #c0392b;
  cursor: pointer;
  font-size: 13px;
  font-family: inherit;
}

.quote-file-previews {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: 14px;
}

.quote-file-preview {
  margin: 0;
  max-width: 120px;
}

.quote-file-preview img {
  width: 100%;
  height: 90px;
  object-fit: cover;
  border-radius: 8px;
  border: 1px solid #e8e8e8;
}

.quote-file-preview figcaption {
  font-size: 11px;
  color: #666;
  margin-top: 4px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
</style>
