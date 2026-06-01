<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import Icon from '@/components/Icon.vue'

const route = useRoute()
const router = useRouter()

const aboutMenuOpen = ref(false)
const navOpen = ref(false)

const isAboutSection = computed(() => route.path.startsWith('/about'))

const aboutDropdownLinks = [
  { label: 'Заказчикам', to: '/about/clients' },
  { label: 'Партнёры', to: '/about/partners' },
  { label: 'Наши преимущества', to: '/about/advantages' },
]

async function goToCallbackForm() {
  if (route.path === '/') {
    await nextTick()
    document.getElementById('callback')?.scrollIntoView({ behavior: 'smooth', block: 'start' })
    return
  }
  await router.push({ path: '/', hash: '#callback' })
}

function closeAboutMenu() {
  aboutMenuOpen.value = false
}

function closeNav() {
  navOpen.value = false
  closeAboutMenu()
}

function toggleNav() {
  navOpen.value = !navOpen.value
}

watch(
  () => route.fullPath,
  () => {
    closeNav()
  },
)
</script>

<template>
  <header class="header" :class="{ 'header--nav-open': navOpen }">
    <div class="container header-top">
      <router-link to="/" class="logo-link">
        <img src="/logo.png" alt="Типография Андрея Христюбова" class="logo" />
      </router-link>

      <div class="contacts-wrapper">
        <div class="contacts-primary">
          <a href="tel:+73832091247" class="contact-item">
            <Icon name="phone" />
            <span>+7 (383) 209-12-47</span>
          </a>
          <a href="tel:+79039345111" class="contact-item">
            <Icon name="mobile" />
            <span>+7 (903) 934-51-11</span>
          </a>
          <a href="mailto:info@tahh.ru" class="contact-item">
            <Icon name="email" />
            <span>info@tahh.ru</span>
          </a>
        </div>
        <div class="contacts-meta">
          <div class="contact-item">
            <Icon name="clock" />
            <span>9:00 – 18:00</span>
          </div>
          <a
            href="https://yandex.ru/maps/?text=ул.%20Большевистская%2C%20131%2C%20к.%206%2C%20Новосибирск"
            class="contact-item contact-item--address"
            target="_blank"
            rel="noopener noreferrer"
          >
            <Icon name="location" />
            <span>ул. Большевистская, 131, к. 6</span>
          </a>
        </div>
      </div>

      <div class="header-top__actions">
        <button type="button" class="callback-btn" @click="goToCallbackForm">
          <span class="callback-btn__full">Заказать звонок</span>
          <span class="callback-btn__short">Звонок</span>
        </button>
        <button
          type="button"
          class="nav-toggle"
          :aria-expanded="navOpen"
          aria-controls="site-nav-menu"
          @click="toggleNav"
        >
          <span class="nav-toggle__line" />
          <span class="nav-toggle__line" />
          <span class="nav-toggle__line" />
          <span class="visually-hidden">{{ navOpen ? 'Закрыть меню' : 'Открыть меню' }}</span>
        </button>
      </div>
    </div>

    <nav
      class="navigation"
      :class="{ 'navigation--open': navOpen }"
      aria-label="Основное меню"
    >
      <div id="site-nav-menu" class="nav-container">
        <router-link to="/" class="nav-item" @click="closeNav">Главная</router-link>
        <router-link to="/catalog" class="nav-item" @click="closeNav">Каталог</router-link>
        <router-link to="/technologies" class="nav-item" @click="closeNav">Технологии</router-link>
        <router-link to="/contacts" class="nav-item" @click="closeNav">Контакты</router-link>

        <div
          class="nav-item-dropdown"
          @mouseenter="aboutMenuOpen = true"
          @mouseleave="aboutMenuOpen = false"
        >
          <router-link
            to="/about"
            class="nav-item"
            :class="{ 'router-link-active': isAboutSection }"
            @click="closeNav"
          >
            О нас
          </router-link>
          <div
            class="nav-dropdown"
            :class="{ 'nav-dropdown--open': aboutMenuOpen }"
            role="menu"
          >
            <router-link
              v-for="link in aboutDropdownLinks"
              :key="link.to"
              :to="link.to"
              class="nav-dropdown__link"
              role="menuitem"
              @click="closeNav"
            >
              {{ link.label }}
            </router-link>
          </div>
        </div>

        <router-link
          v-for="link in aboutDropdownLinks"
          :key="`m-${link.to}`"
          :to="link.to"
          class="nav-item nav-item--mobile-sub"
          @click="closeNav"
        >
          {{ link.label }}
        </router-link>

        <router-link to="/vacancies" class="nav-item" @click="closeNav">Вакансии</router-link>
        <router-link to="/graphic-module" class="nav-item" @click="closeNav">Графический модуль</router-link>
      </div>
    </nav>
  </header>
</template>
