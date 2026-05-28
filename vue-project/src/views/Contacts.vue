<script setup lang="ts">
import { ref } from 'vue'
import RuPhoneInput from '@/components/RuPhoneInput.vue'
import { isRuPhoneComplete } from '@/utils/ruPhone'

const form = ref({
  name: '',
  email: '',
  phone: '',
  message: ''
})

const submitForm = () => {
  if (!isRuPhoneComplete(form.value.phone)) {
    alert('Укажите полный номер телефона в формате +7 (999) 999-99-99')
    return
  }
  alert('Спасибо! Ваше сообщение отправлено. Мы свяжемся с вами в ближайшее время.')
  form.value = { name: '', email: '', phone: '', message: '' }
}

const contactInfo = [
  {
    icon: 'phone',
    title: 'Телефон',
    items: [
      { label: '+7 (383) 209-12-47', href: 'tel:+73832091247' },
      { label: '+7 (903) 934-51-11', href: 'tel:+79039345111' }
    ]
  },
  {
    icon: 'email',
    title: 'Email',
    items: [
      { label: 'info@tahh.ru', href: 'mailto:info@tahh.ru' }
    ]
  },
  {
    icon: 'location',
    title: 'Адрес',
    items: [
      { label: '630083, г.Новосибирск, ул. Большевистская, 131, корпус 6', href: '#' }
    ]
  },
  {
    icon: 'clock',
    title: 'Режим работы',
    items: [
      { label: 'Пн-Пт: 9:00 - 18:00', href: '#' },
      { label: 'Сб-Вс: Выходной', href: '#' }
    ]
  }
]
</script>

<template>
  <div class="app">
    <main class="main-content">
      <div class="container">
        <!-- Заголовок страницы -->
        <h1 class="page-title">Контакты</h1>
        <p class="page-subtitle">Свяжитесь с нами любым удобным способом</p>

        <div class="visualization-block contacts-quote-strip">
          <span class="visualization-text">
            Нужен расчёт тиража? Быстрый расчёт — параметры заказа и коммерческое предложение
          </span>
          <router-link to="/quick-quote" class="visualization-btn">
            Быстрый расчёт <span class="btn-arrow">→</span>
          </router-link>
        </div>

        <div class="contacts-layout">
          <!-- Левая часть: Контактная информация -->
          <div class="contacts-info">
            <div class="info-cards">
              <div v-for="contact in contactInfo" :key="contact.title" class="info-card">
                <div class="info-icon">
                  <svg v-if="contact.icon === 'phone'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/>
                  </svg>
                  <svg v-else-if="contact.icon === 'email'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/>
                    <polyline points="22,6 12,13 2,6"/>
                  </svg>
                  <svg v-else-if="contact.icon === 'location'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/>
                    <circle cx="12" cy="10" r="3"/>
                  </svg>
                  <svg v-else-if="contact.icon === 'clock'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="12" cy="12" r="10"/>
                    <polyline points="12 6 12 12 16 14"/>
                  </svg>
                </div>
                <div class="info-content">
                  <h3 class="info-title">{{ contact.title }}</h3>
                  <div class="info-items">
                    <a v-for="item in contact.items" :key="item.label" :href="item.href" class="info-item">
                      {{ item.label }}
                    </a>
                  </div>
                </div>
              </div>
            </div>

            <!-- Социальные сети -->
            <div class="social-section">
              <h3 class="social-title">Мы в социальных сетях</h3>
              <div class="social-links">
                <a href="https://vk.com" target="_blank" rel="noopener noreferrer" class="social-link vk" aria-label="ВКонтакте">
                  <svg viewBox="0 0 24 24" aria-hidden="true">
                    <rect width="24" height="24" rx="5.5" fill="currentColor" />
                    <path
                      fill="#fff"
                      d="M6.79 7.3H4.05c.13 6.24 3.25 9.99 8.72 9.99h.31v-3.57c2.01.2 3.53 1.67 4.14 3.57h2.84c-.78-2.84-2.83-4.41-4.11-5.01 1.28-.74 3.08-2.54 3.51-4.98h-2.58c-.56 1.98-2.22 3.78-3.8 3.95V7.3H10.5v6.92c-1.6-.4-3.62-2.34-3.71-6.92Z"
                    />
                  </svg>
                </a>
                <a href="https://t.me" target="_blank" class="social-link telegram">
                  <svg viewBox="0 0 24 24" fill="currentColor">
                    <path d="M11.944 0A12 12 0 0 0 0 12a12 12 0 0 0 12 12 12 12 0 0 0 12-12A12 12 0 0 0 12 0a12 12 0 0 0-.056 0zm4.962 7.224c.1-.002.321.023.465.14a.506.506 0 0 1 .171.325c.016.093.036.306.02.472-.18 1.898-.962 6.502-1.36 8.627-.168.9-.499 1.201-.82 1.23-.696.065-1.225-.46-1.9-.902-1.056-.693-1.653-1.124-2.678-1.8-1.185-.78-.417-1.21.258-1.91.177-.184 3.247-2.977 3.307-3.23.007-.032.014-.15-.056-.212s-.174-.041-.249-.024c-.106.024-1.793 1.14-5.061 3.345-.48.33-.913.49-1.302.48-.428-.008-1.252-.241-1.865-.44-.752-.245-1.349-.374-1.297-.789.027-.216.325-.437.893-.663 3.498-1.524 5.83-2.529 6.998-3.014 3.332-1.386 4.025-1.627 4.476-1.635z"/>
                  </svg>
                </a>
                <a href="https://youtube.com" target="_blank" class="social-link youtube">
                  <svg viewBox="0 0 24 24" fill="currentColor">
                    <path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/>
                  </svg>
                </a>
              </div>
            </div>
          </div>

          <!-- Правая часть: Форма обратной связи -->
          <div class="contacts-form-wrapper">
            <div class="contacts-form-container">
              <h2 class="form-title">Напишите нам</h2>
              <p class="form-subtitle">Заполните форму и мы свяжемся с вами в ближайшее время</p>
              
              <form class="contacts-form" @submit.prevent="submitForm">
                <div class="form-group">
                  <label for="name" class="form-label">Полное имя *</label>
                  <input 
                    id="name"
                    v-model="form.name"
                    type="text" 
                    placeholder="Иванов Иван Иванович"
                    class="form-input"
                    required
                  />
                </div>

                <div class="form-group">
                  <label for="email" class="form-label">Email *</label>
                  <input 
                    id="email"
                    v-model="form.email"
                    type="email" 
                    placeholder="example@mail.ru"
                    class="form-input"
                    required
                  />
                </div>

                <div class="form-group">
                  <label for="phone" class="form-label">Номер телефона *</label>
                  <RuPhoneInput id="phone" v-model="form.phone" required />
                </div>

                <div class="form-group">
                  <label for="message" class="form-label">Сообщение *</label>
                  <textarea 
                    id="message"
                    v-model="form.message"
                    placeholder="Введите ваше сообщение..."
                    class="form-textarea"
                    rows="5"
                    required
                  ></textarea>
                </div>

                <button type="submit" class="submit-button">
                  Отправить сообщение
                  <svg class="button-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <line x1="22" y1="2" x2="11" y2="13"/>
                    <polygon points="22 2 15 22 11 13 2 9 22 2"/>
                  </svg>
                </button>
              </form>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<style scoped>
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
  margin-bottom: 30px;
}

.contacts-quote-strip {
  margin-bottom: 40px;
}

.contacts-layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 50px;
  margin-bottom: 60px;
}

/* Левая часть: Контактная информация */
.contacts-info {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.info-cards {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.info-card {
  display: flex;
  gap: 20px;
  padding: 25px;
  background: #f5f5f5;
  border-radius: 15px;
  transition: all 0.3s;
  border-left: 4px solid #ff7722;
}

.info-card:hover {
  transform: translateX(10px);
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
}

.info-icon {
  width: 50px;
  height: 50px;
  background: #ff7722;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.info-icon svg {
  width: 26px;
  height: 26px;
  color: white;
}

.info-content {
  flex: 1;
}

.info-title {
  font-size: 18px;
  font-weight: 600;
  color: #333;
  margin-bottom: 10px;
  font-family: var(--font-heading);
}

.info-items {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.info-item {
  color: #666;
  text-decoration: none;
  font-size: 15px;
  transition: color 0.3s;
}

.info-item:hover {
  color: #ff7722;
}

/* Социальные сети */
.social-section {
  background: linear-gradient(135deg, #ff7722 0%, #ff9955 100%);
  padding: 30px;
  border-radius: 15px;
  text-align: center;
}

.social-title {
  font-size: 18px;
  color: white;
  margin-bottom: 20px;
  font-weight: 600;
}

.social-links {
  display: flex;
  justify-content: center;
  gap: 15px;
}

.social-link {
  width: 50px;
  height: 50px;
  background: white;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
}

.social-link svg {
  width: 26px;
  height: 26px;
}

.social-link.vk svg {
  color: #0077ff;
}

.social-link.telegram svg {
  color: #0088cc;
}

.social-link.youtube svg {
  color: #FF0000;
}

.social-link:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

/* Правая часть: Форма */
.contacts-form-wrapper {
  background: #f5f5f5;
  border-radius: 20px;
  padding: 40px;
}

.contacts-form-container {
  max-width: 100%;
}

.form-title {
  font-size: 28px;
  color: #333;
  margin-bottom: 10px;
  font-family: var(--font-heading);
}

.form-subtitle {
  font-size: 15px;
  color: #666;
  margin-bottom: 30px;
}

.contacts-form {
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
.form-textarea {
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
.form-textarea:focus {
  border-color: #ff7722;
  box-shadow: 0 0 0 3px rgba(255, 119, 34, 0.1);
}

.form-textarea {
  resize: vertical;
  min-height: 120px;
}

.submit-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  background: #ff7722;
  color: white;
  padding: 15px 35px;
  border-radius: 25px;
  border: none;
  cursor: pointer;
  font-size: 16px;
  font-weight: 500;
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

/* Адаптивность */
@media (max-width: 992px) {
  .contacts-layout {
    grid-template-columns: 1fr;
    gap: 40px;
  }
}

@media (max-width: 640px) {
  .page-title {
    font-size: 32px;
  }
  
  .page-subtitle {
    font-size: 16px;
  }
  
  .contacts-form-wrapper {
    padding: 25px;
  }
  
  .info-card {
    padding: 20px;
  }
  
  .info-icon {
    width: 45px;
    height: 45px;
  }
  
  .social-links {
    gap: 10px;
  }
  
  .social-link {
    width: 45px;
    height: 45px;
  }
}
</style>