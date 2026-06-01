<script setup lang="ts">
import { useRoute, useRouter } from 'vue-router'
import { useAuth } from '@/composables/useAuth'

const route = useRoute()
const router = useRouter()
const { user, logout } = useAuth()

const navItems = [
  { to: '/staff/inbox', label: 'Заявки', exact: false },
  { to: '/staff/admin/catalog', label: 'Каталог', exact: false },
  { to: '/staff/admin/portfolio', label: 'Готовые работы', exact: false },
  { to: '/staff/admin/chat', label: 'Чат-бот', exact: false },
]

function linkActive(path: string) {
  return route.path.startsWith(path)
}

async function doLogout() {
  await logout()
  await router.push('/staff/login')
}
</script>

<template>
  <div class="staff-layout">
    <header class="staff-bar">
      <div class="container staff-bar-inner">
        <div>
          <h1>Управление сайтом</h1>
          <p v-if="user" class="staff-user">{{ user.first_name || user.username }}</p>
        </div>
        <div class="staff-bar-actions">
          <router-link to="/staff/inbox" class="staff-link-btn">Заявки</router-link>
          <router-link to="/" class="staff-link-btn">Сайт</router-link>
          <button type="button" class="staff-link-btn" @click="doLogout">Выйти</button>
        </div>
      </div>
    </header>

    <div class="container staff-admin-wrap">
      <nav class="staff-admin-nav" aria-label="Разделы управления">
        <router-link
          v-for="item in navItems"
          :key="item.to"
          :to="item.to"
          class="staff-admin-nav__link"
          :class="{ active: linkActive(item.to) }"
        >
          {{ item.label }}
        </router-link>
      </nav>
      <main class="staff-admin-main">
        <slot />
      </main>
    </div>
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
  padding: 16px 0;
}
.staff-bar-inner {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 16px;
}
.staff-bar h1 {
  font-size: 1.35rem;
}
.staff-user {
  color: #666;
  font-size: 0.85rem;
}
.staff-bar-actions {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}
.staff-link-btn {
  padding: 8px 14px;
  background: #eee;
  border: none;
  border-radius: 6px;
  text-decoration: none;
  color: #333;
  font-size: 0.9rem;
  cursor: pointer;
}
.staff-admin-wrap {
  display: grid;
  grid-template-columns: 200px 1fr;
  gap: 24px;
  padding: 24px 20px 48px;
  align-items: start;
}
.staff-admin-nav {
  display: flex;
  flex-direction: column;
  gap: 6px;
  background: #fff;
  border-radius: 10px;
  padding: 12px;
  border: 1px solid #e8e8e8;
}
.staff-admin-nav__link {
  padding: 10px 12px;
  border-radius: 8px;
  text-decoration: none;
  color: #333;
  font-size: 0.92rem;
}
.staff-admin-nav__link.active {
  background: #f72;
  color: #fff;
}
.staff-admin-main {
  min-width: 0;
}
@media (max-width: 768px) {
  .staff-admin-wrap {
    grid-template-columns: 1fr;
  }
  .staff-admin-nav {
    flex-direction: row;
    flex-wrap: wrap;
  }
}
</style>
