<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import RuPhoneInput from '@/components/RuPhoneInput.vue'
import { apiFetch } from '@/api/http'
import { isRuPhoneComplete, ruPhoneForApi } from '@/utils/ruPhone'

const router = useRouter()

const form = ref({
  fullName: '',
  age: '',
  education: '',
  position: '',
  salary: '',
  experience: '',
  phone: '',
  consent: false,
})

const loading = ref(false)
const error = ref('')
const success = ref(false)

async function submitForm() {
  if (!form.value.consent) {
    error.value = 'Подтвердите согласие на обработку персональных данных'
    return
  }
  if (!isRuPhoneComplete(form.value.phone)) {
    error.value = 'Укажите полный номер телефона в формате +7 (999) 999-99-99'
    return
  }

  loading.value = true
  error.value = ''
  success.value = false

  try {
    await apiFetch('/send-resume/', {
      method: 'POST',
      body: JSON.stringify({
        full_name: form.value.fullName.trim(),
        age: Number(form.value.age),
        education: form.value.education.trim(),
        position: form.value.position,
        salary: form.value.salary.trim(),
        experience: form.value.experience,
        phone: ruPhoneForApi(form.value.phone),
      }),
    })
    success.value = true
    form.value = {
      fullName: '',
      age: '',
      education: '',
      position: '',
      salary: '',
      experience: '',
      phone: '',
      consent: false,
    }
    setTimeout(() => router.push('/vacancies'), 2500)
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Не удалось отправить резюме'
  } finally {
    loading.value = false
  }
}

const experienceOptions = [
  'Нет опыта',
  'До 1 года',
  '1-3 года',
  '3-5 лет',
  'Более 5 лет'
]

const positionOptions = [
  'Менеджер по продажам',
  'Дизайнер полиграфии',
  'Оператор печатной машины',
  'Менеджер по работе с клиентами',
  'Бухгалтер',
  'Другое'
]
</script>

<template>
  <div class="app">
    <main class="main-content">
      <div class="container">
        <!-- Заголовок страницы -->
        <h1 class="page-title">Отправить резюме</h1>
        <p class="page-subtitle">Заполните форму и станьте частью нашей команды</p>

        <div class="resume-form-wrapper">
          <div class="resume-form-container">
            <p v-if="success" class="resume-alert resume-alert--ok" role="status">
              Спасибо! Резюме отправлено на почту типографии. Мы свяжемся с вами в ближайшее время.
            </p>
            <p v-if="error" class="resume-alert resume-alert--err" role="alert">{{ error }}</p>

            <form class="resume-form" @submit.prevent="submitForm">
              <!-- ФИО -->
              <div class="form-group">
                <label for="fullName" class="form-label">ФИО *</label>
                <input 
                  id="fullName"
                  v-model="form.fullName"
                  type="text" 
                  placeholder="Иванов Иван Иванович"
                  class="form-input"
                  required
                />
              </div>

              <!-- Возраст -->
              <div class="form-group">
                <label for="age" class="form-label">Возраст *</label>
                <input 
                  id="age"
                  v-model="form.age"
                  type="number" 
                  placeholder="25"
                  class="form-input"
                  min="18"
                  max="70"
                  required
                />
              </div>

              <!-- Желаемая должность -->
              <div class="form-group">
                <label for="position" class="form-label">Желаемая должность *</label>
                <select 
                  id="position"
                  v-model="form.position"
                  class="form-input form-select"
                  required
                >
                  <option value="" disabled>Выберите должность</option>
                  <option v-for="pos in positionOptions" :key="pos" :value="pos">{{ pos }}</option>
                </select>
              </div>

              <!-- Желаемый уровень зарплаты -->
              <div class="form-group">
                <label for="salary" class="form-label">Желаемый уровень зарплаты (₽) *</label>
                <input 
                  id="salary"
                  v-model="form.salary"
                  type="text" 
                  placeholder="60 000"
                  class="form-input"
                  required
                />
              </div>

              <!-- Основное образование -->
              <div class="form-group">
                <label for="education" class="form-label">Основное образование *</label>
                <input 
                  id="education"
                  v-model="form.education"
                  type="text" 
                  placeholder="Высшее, Среднее специальное и т.д."
                  class="form-input"
                  required
                />
              </div>

              <!-- Опыт работы -->
              <div class="form-group">
                <label for="experience" class="form-label">Опыт работы в типографии *</label>
                <select 
                  id="experience"
                  v-model="form.experience"
                  class="form-input form-select"
                  required
                >
                  <option value="" disabled>Выберите вариант</option>
                  <option v-for="exp in experienceOptions" :key="exp" :value="exp">{{ exp }}</option>
                </select>
              </div>

              <!-- Телефон WhatsApp -->
              <div class="form-group">
                <label for="phone" class="form-label">Номер телефона для связи в WhatsApp *</label>
                <RuPhoneInput id="phone" v-model="form.phone" required />
                <span class="form-hint">Укажите номер, привязанный к WhatsApp</span>
              </div>

              <!-- Согласие на обработку данных -->
              <div class="form-group form-checkbox">
                <label class="checkbox-label">
                  <input 
                    type="checkbox" 
                    v-model="form.consent"
                    required
                  />
                  <span class="checkbox-text">
                    Выражаю согласие на обработку моих персональных данных в соответствии с 
                    <a href="https://base.garant.ru/12148567/" target="_blank" class="link">
                      Федеральным законом "О персональных данных" от 27.07.2006г. №152-ФЗ
                    </a>
                  </span>
                </label>
              </div>

              <!-- Кнопка отправки -->
              <button type="submit" class="submit-button" :disabled="loading || success">
                {{ loading ? 'Отправка…' : 'Отправить резюме' }}
                <svg class="button-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <line x1="22" y1="2" x2="11" y2="13"/>
                  <polygon points="22 2 15 22 11 13 2 9 22 2"/>
                </svg>
              </button>
            </form>
          </div>

          <!-- Дополнительная информация -->
          <div class="resume-info">
            <h3 class="info-title">Что будет дальше?</h3>
            <div class="info-steps">
              <div class="info-step">
                <div class="step-number">1</div>
                <div class="step-content">
                  <h4>Рассмотрение резюме</h4>
                  <p>Мы изучим вашу анкету в течение 1-2 рабочих дней</p>
                </div>
              </div>
              <div class="info-step">
                <div class="step-number">2</div>
                <div class="step-content">
                  <h4>Связь с вами</h4>
                  <p>Позвоним или напишем в WhatsApp для уточнения деталей</p>
                </div>
              </div>
              <div class="info-step">
                <div class="step-number">3</div>
                <div class="step-content">
                  <h4>Собеседование</h4>
                  <p>Пригласим на встречу в офис или проведём онлайн</p>
                </div>
              </div>
              <div class="info-step">
                <div class="step-number">4</div>
                <div class="step-content">
                  <h4>Трудоустройство</h4>
                  <p>Оформим документы и начнём работу</p>
                </div>
              </div>
            </div>

            <div class="info-contact">
              <p>Есть вопросы? Звоните:</p>
              <a href="tel:+73832091247" class="contact-phone">+7 (383) 209-12-47</a>
              <p class="contact-hours">Пн-Пт: 9:00 - 18:00</p>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<style scoped>
.resume-alert {
  margin: 0 0 20px;
  padding: 12px 16px;
  border-radius: 8px;
  font-size: 0.95rem;
  line-height: 1.45;
}

.resume-alert--ok {
  background: #e8f8ee;
  border: 1px solid #9fd4b0;
  color: #1a6b34;
}

.resume-alert--err {
  background: #fff0f0;
  border: 1px solid #f0b4b4;
  color: #a52a2a;
}

.page-title {
  font-size: 42px;
  color: #008000;
  text-align: center;
  margin-bottom: 10px;
  font-family: var(--font-heading);
}

.page-subtitle {
  font-size: 18px;
  color: #666;
  text-align: center;
  margin-bottom: 50px;
}

.resume-form-wrapper {
  display: grid;
  grid-template-columns: 1fr 400px;
  gap: 40px;
  margin-bottom: 60px;
}

.resume-form-container {
  background: #f5f5f5;
  border-radius: 20px;
  padding: 40px;
}

.resume-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-label {
  font-size: 14px;
  color: #333;
  font-weight: 500;
}

.form-input,
.form-select {
  padding: 15px 20px;
  border: 2px solid #e8e8e8;
  border-radius: 12px;
  font-size: 15px;
  background: white;
  outline: none;
  transition: all 0.3s;
  font-family: var(--font-body);
}

.form-input:focus,
.form-select:focus {
  border-color: #ff7722;
  box-shadow: 0 0 0 3px rgba(255, 119, 34, 0.1);
}

.form-select {
  cursor: pointer;
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'%3E%3Cpath fill='%23666' d='M6 8L1 3h10z'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 15px center;
  padding-right: 40px;
}

.form-hint {
  font-size: 12px;
  color: #999;
  margin-top: -5px;
}

/* Чекбокс */
.form-checkbox {
  margin-top: 10px;
}

.checkbox-label {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  cursor: pointer;
}

.checkbox-label input[type="checkbox"] {
  width: 20px;
  height: 20px;
  margin-top: 2px;
  cursor: pointer;
  accent-color: #ff7722;
}

.checkbox-text {
  font-size: 13px;
  color: #666;
  line-height: 1.6;
}

.checkbox-text .link {
  color: #ff7722;
  text-decoration: underline;
}

.checkbox-text .link:hover {
  color: #e66611;
}

/* Кнопка */
.submit-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  background: #ff7722;
  color: white;
  padding: 16px 40px;
  border-radius: 25px;
  border: none;
  cursor: pointer;
  font-size: 16px;
  font-weight: 600;
  transition: all 0.3s;
  margin-top: 10px;
}

.submit-button:hover {
  background: #e66611;
  transform: translateY(-3px);
  box-shadow: 0 5px 20px rgba(255, 119, 34, 0.4);
}

.button-icon {
  width: 20px;
  height: 20px;
}

/* Правая панель с информацией */
.resume-info {
  background: linear-gradient(135deg, #008000 0%, #00aa44 100%);
  border-radius: 20px;
  padding: 35px;
  color: white;
}

.info-title {
  font-size: 22px;
  font-weight: 600;
  margin-bottom: 25px;
  font-family: var(--font-heading);
}

.info-steps {
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin-bottom: 30px;
}

.info-step {
  display: flex;
  gap: 15px;
  align-items: flex-start;
}

.step-number {
  width: 35px;
  height: 35px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  font-weight: 600;
  flex-shrink: 0;
}

.step-content h4 {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 5px;
}

.step-content p {
  font-size: 13px;
  opacity: 0.9;
  line-height: 1.5;
}

.info-contact {
  border-top: 1px solid rgba(255, 255, 255, 0.3);
  padding-top: 25px;
  text-align: center;
}

.info-contact p {
  font-size: 14px;
  opacity: 0.9;
  margin-bottom: 10px;
}

.contact-phone {
  display: block;
  font-size: 20px;
  font-weight: 600;
  color: white;
  text-decoration: none;
  margin-bottom: 8px;
  transition: opacity 0.3s;
}

.contact-phone:hover {
  opacity: 0.8;
}

.contact-hours {
  font-size: 13px;
  opacity: 0.8;
}

/* Адаптивность */
@media (max-width: 992px) {
  .resume-form-wrapper {
    grid-template-columns: 1fr;
  }
  
  .resume-info {
    order: -1;
  }
}

@media (max-width: 640px) {
  .page-title {
    font-size: 32px;
  }
  
  .resume-form-container {
    padding: 25px;
  }
  
  .resume-info {
    padding: 25px;
  }
  
  .info-title {
    font-size: 20px;
  }
  
  .step-content h4 {
    font-size: 15px;
  }
  
  .step-content p {
    font-size: 12px;
  }
}
</style>