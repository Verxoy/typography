<script setup lang="ts">
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuth } from '@/composables/useAuth'

const { login, loading } = useAuth()
const router = useRouter()
const route = useRoute()

const username = ref('')
const password = ref('')
const error = ref('')

async function onSubmit() {
  error.value = ''
  try {
    await login(username.value.trim(), password.value)
    const redirect = (route.query.redirect as string) || '/staff/inbox'
    router.push(redirect)
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Ошибка входа'
  }
}
</script>

<template>
  <div class="staff-page">
    <div class="staff-card">
      <h1>Вход для сотрудников</h1>
      <p class="staff-hint">Раздел заявок «Быстрый расчёт» доступен только менеджерам типографии.</p>
      <form @submit.prevent="onSubmit">
        <label class="staff-field">
          <span>Логин</span>
          <input v-model="username" type="text" autocomplete="username" required />
        </label>
        <label class="staff-field">
          <span>Пароль</span>
          <input v-model="password" type="password" autocomplete="current-password" required />
        </label>
        <p v-if="error" class="staff-error">{{ error }}</p>
        <button type="submit" class="staff-btn" :disabled="loading">
          {{ loading ? 'Вход…' : 'Войти' }}
        </button>
      </form>
      <router-link to="/" class="staff-link">← На сайт</router-link>
    </div>
  </div>
</template>

<style scoped>
.staff-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f0f0f0;
  padding: 20px;
}
.staff-card {
  background: #fff;
  padding: 36px;
  border-radius: 12px;
  width: 100%;
  max-width: 400px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
}
.staff-card h1 {
  font-size: 1.5rem;
  margin-bottom: 8px;
}
.staff-hint {
  color: #666;
  font-size: 0.9rem;
  margin-bottom: 24px;
}
.staff-field {
  display: block;
  margin-bottom: 16px;
}
.staff-field span {
  display: block;
  margin-bottom: 6px;
  font-size: 0.9rem;
}
.staff-field input {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
}
.staff-error {
  color: #c0392b;
  margin-bottom: 12px;
  font-size: 0.9rem;
}
.staff-btn {
  width: 100%;
  padding: 12px;
  background: #ff7722;
  color: #fff;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
}
.staff-btn:disabled {
  opacity: 0.7;
}
.staff-link {
  display: block;
  margin-top: 20px;
  text-align: center;
  color: #666;
}
</style>
