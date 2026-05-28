<script setup lang="ts">
import { computed, nextTick, onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import RuPhoneInput from '@/components/RuPhoneInput.vue'
import PortfolioShowcase from '@/components/PortfolioShowcase.vue'
import { apiFetch } from '@/api/http'
import { usePublicCatalog } from '@/composables/usePublicCatalog'
import { isRuPhoneComplete, ruPhoneForApi } from '@/utils/ruPhone'
import { CATALOG_SECTION_BY_TITLE } from '../data/catalog'
import {
  HOME_CATALOG_FALLBACK_IMAGES,
  HOME_CATALOG_SECTION_TITLES,
} from '@/data/homeCatalogSections'

const homeBannerImage = '/images/home-banner-calendars-2025.jpg'
const quotePromoImage = '/images/quick-quote-promo.png'
const quotePromoImageOk = ref(true)

function onQuotePromoImageError() {
  quotePromoImageOk.value = false
}

const route = useRoute()
const form = ref({ name: '', phone: '' })
const submitting = ref(false)
const submitError = ref('')
const submitSuccess = ref(false)

async function scrollToCallback() {
  await nextTick()
  document.getElementById('callback')?.scrollIntoView({ behavior: 'smooth', block: 'start' })
}

onMounted(() => {
  void loadCatalogFromApi()
  if (route.hash === '#callback') {
    void scrollToCallback()
  }
})

watch(
  () => route.hash,
  (hash) => {
    if (hash === '#callback') void scrollToCallback()
  },
)

const submitForm = async () => {
  submitError.value = ''
  submitSuccess.value = false
  if (!isRuPhoneComplete(form.value.phone)) {
    submitError.value = 'Укажите полный номер телефона в формате +7 (999) 999-99-99'
    return
  }
  submitting.value = true
  try {
    await apiFetch<{ message: string }>('/request-callback/', {
      method: 'POST',
      body: JSON.stringify({
        name: form.value.name.trim(),
        phone: ruPhoneForApi(form.value.phone),
      }),
    })
    submitSuccess.value = true
    form.value = { name: '', phone: '' }
  } catch (e) {
    submitError.value = e instanceof Error ? e.message : 'Не удалось отправить заявку'
  } finally {
    submitting.value = false
  }
}

const { apiSections, loadCatalogFromApi } = usePublicCatalog()

const categories = computed(() => {
  const homeImageByTitle = new Map(
    (apiSections.value ?? []).map((s) => [s.title, s.homeImageUrl]),
  )
  return HOME_CATALOG_SECTION_TITLES.map((name) => {
    const section = CATALOG_SECTION_BY_TITLE[name]
    const image =
      homeImageByTitle.get(name) || HOME_CATALOG_FALLBACK_IMAGES[name] || ''
    return {
      name,
      image,
      link: section ? { path: '/catalog', query: { section: name } } : '/catalog',
    }
  })
})
</script>

<template>
  <div class="app">
    <main class="main-content">
      <div class="container">
        <!-- Баннер -->
        <section class="banner banner--hero" aria-label="Промо-баннер">
          <button type="button" class="banner-btn banner-btn--prev" aria-label="Предыдущий слайд">
            ←
          </button>
          <div class="banner-media">
            <img
              :src="homeBannerImage"
              alt="Календари на 2025 год — типография Андрея Христолюбова"
              class="banner-image"
              width="1200"
              height="400"
              fetchpriority="high"
            />
          </div>
          <button type="button" class="banner-btn banner-btn--next" aria-label="Следующий слайд">
            →
          </button>
        </section>

        <!-- Карточки категорий -->
        <div class="categories-section">
          <div class="categories-grid">
            <div 
              v-for="category in categories" 
              :key="category.name"
              class="category-card"
            >
              <router-link :to="category.link" class="category-link">
                <h3 class="category-title">{{ category.name }}</h3>
                <div v-if="category.image" class="category-image">
                  <img :src="category.image" :alt="category.name" loading="lazy" />
                </div>
                <div v-else class="category-image-placeholder" />
              </router-link>
            </div>
          </div>
        </div>

        <!-- Модуль визуализации -->
        <div class="visualization-section">
          <div class="visualization-block">
            <span class="visualization-text">Увидеть, как будет выглядеть ваш заказ</span>
            <router-link to="/graphic-module" class="visualization-btn">
              Графический модуль <span class="btn-arrow">→</span>
            </router-link>
          </div>
        </div>
      </div>

      <!-- Форма обратной связи (ВНЕ container - на всю ширину) -->
      <div id="callback" class="callback-section">
        <div class="callback-container">
          <div class="container">
            <div class="callback-left">
              <h2 class="callback-title">Заполните заявку и<br>мы вам <span class="highlight">перезвоним</span></h2>
              <p class="callback-alt">
                Нужен расчёт тиража?
                <router-link to="/quick-quote" class="callback-alt-link">Быстрый расчёт</router-link>
                — параметры заказа и коммерческое предложение
              </p>
            </div>
            <div class="callback-right">
              <form class="callback-form" @submit.prevent="submitForm">
                <input v-model="form.name" type="text" placeholder="Имя" class="form-input" required />
                <RuPhoneInput v-model="form.phone" required />
                <p v-if="submitError" class="callback-form-msg callback-form-msg--error">{{ submitError }}</p>
                <p v-else-if="submitSuccess" class="callback-form-msg callback-form-msg--ok">
                  Спасибо! Мы перезвоним вам в ближайшее время.
                </p>
                <button type="submit" class="submit-btn" :disabled="submitting">
                  {{ submitting ? 'Отправка…' : 'Заказать звонок' }}
                </button>
              </form>
            </div>
          </div>
        </div>
      </div>

      <div class="container">
        <!-- Преимущества -->
        <div class="about-section">
          <div class="about-container">
            <h2 class="about-title">Типография Андрея Христюбова в Новосибирске</h2>
            <p class="about-description">Мы специализируемся на работе с юридическими лицами и ИП. Более 20 лет опыта гарантируют стабильное качество.</p>
            <div class="features-grid">
              <div class="feature-item">
                <div class="feature-icon">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
                </div>
                <h3 class="feature-title">Сжатые сроки<br>исполнения заказов</h3>
              </div>
              <div class="feature-item">
                <div class="feature-icon">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="3" width="20" height="14" rx="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg>
                </div>
                <h3 class="feature-title">Заказ онлайн - без<br>визита в офис</h3>
              </div>
              <div class="feature-item">
                <div class="feature-icon">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="1" y="3" width="15" height="13"/><polygon points="16 8 20 8 23 11 23 16 16 16 16 8"/><circle cx="5.5" cy="18.5" r="2.5"/><circle cx="18.5" cy="18.5" r="2.5"/></svg>
                </div>
                <h3 class="feature-title">Бесплатная доставка при<br>заказе от 30 000 ₽</h3>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Быстрый расчёт — карточка перед блоком «О компании» -->
      <section class="quote-promo-section">
        <div class="container">
          <article class="quote-promo-card">
            <div class="quote-promo-card__media">
              <img
                v-if="quotePromoImageOk"
                :src="quotePromoImage"
                alt="Быстрый расчёт заказа в типографии"
                @error="onQuotePromoImageError"
              />
              <div v-else class="quote-promo-card__placeholder">
                <span>Фотография скоро появится</span>
              </div>
            </div>
            <div class="quote-promo-card__content">
              <h2 class="quote-promo-card__title">Быстрый расчёт</h2>
              <p class="quote-promo-card__text">
                Кратко опишите задачу — не обязательно знать все параметры заранее.
                Три простых шага без регистрации: подготовим коммерческое предложение,
                менеджер свяжется с вами.
              </p>
              <router-link to="/quick-quote" class="visualization-btn quote-promo-card__btn">
                Перейти к расчёту <span class="btn-arrow">→</span>
              </router-link>
            </div>
          </article>
        </div>
      </section>

      <PortfolioShowcase />

      <!-- О компании (ВНЕ container - на всю ширину) -->
      <div class="company-section">
        <div class="company-container">
          <div class="container">
            <div class="company-grid">
              <div class="company-image">
                <img src="/images/dude.png" alt="Основатель" />
              </div>
              <div class="company-content">
                <h2 class="company-title">О компании</h2>
                <p class="company-text">
                  Мы работаем на полиграфическом рынке Новосибирска с 2000 года. С момента основания 
                  наша цель неизменна — создавать современное гибкое предприятие, выпускающее 
                  рекламно-акцидентную продукцию высокого качества по разумным ценам. Это стало 
                  возможным благодаря команде экспертов в области дизайна и печатных технологий, 
                  для которых нет невыполнимых задач. Наше кредо — находить простые и технологичные 
                  решения даже в самых сложных ситуациях.
                </p>
                <div class="company-features">
                  <div class="company-feature">
                    <span class="feature-star">⭐</span>
                    <span class="feature-text">Звание «Мэтр полиграфии» — подтверждение статуса Мастера.</span>
                  </div>
                  <div class="company-feature">
                    <span class="feature-star">⭐</span>
                    <span class="feature-text">Награды «Сибирской Ярмарки» — дипломы и медали за качество.</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<style scoped>
.callback-alt {
  margin-top: 16px;
  font-size: 15px;
  color: #555;
  line-height: 1.5;
  max-width: 420px;
}

.callback-alt-link {
  color: #ff7722;
  font-weight: 600;
  text-decoration: underline;
  text-underline-offset: 3px;
}

.callback-alt-link:hover {
  color: #e66611;
}

.callback-form-msg {
  margin: 0;
  font-size: 14px;
  line-height: 1.4;
}
.callback-form-msg--error {
  color: #c62828;
}
.callback-form-msg--ok {
  color: #2e7d32;
}
</style>