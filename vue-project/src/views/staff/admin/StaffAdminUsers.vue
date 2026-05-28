<script setup lang="ts">

import { onMounted, ref } from 'vue'

import { apiFetch } from '@/api/http'

import StaffAdminShell from '@/components/staff/StaffAdminShell.vue'



type StaffUserRow = {

  id: number

  username: string

  first_name: string

  email: string

  is_active: boolean

  is_administrator: boolean

  is_manager: boolean

}



const users = ref<StaffUserRow[]>([])

const message = ref('')



const newUser = ref({

  username: '',

  first_name: '',

  email: '',

  password: '',

  is_administrator: false,

  is_manager: true,

  is_active: true,

})



async function load() {

  users.value = await apiFetch<StaffUserRow[]>('/staff/cms/users/')

}



async function saveUser(u: StaffUserRow) {

  await apiFetch(`/staff/cms/users/${u.id}/`, {

    method: 'PATCH',

    body: JSON.stringify({

      first_name: u.first_name,

      email: u.email,

      is_active: u.is_active,

      is_administrator: u.is_administrator,

      is_manager: u.is_manager,

    }),

  })

  message.value = 'Сохранено'

}



async function createUser() {

  if (!newUser.value.username.trim() || !newUser.value.password) return

  await apiFetch('/staff/cms/users/', {

    method: 'POST',

    body: JSON.stringify(newUser.value),

  })

  newUser.value = {

    username: '',

    first_name: '',

    email: '',

    password: '',

    is_administrator: false,

    is_manager: true,

    is_active: true,

  }

  await load()

  message.value = 'Пользователь создан'

}

async function deactivateUser(u: StaffUserRow) {
  if (!confirm(`Деактивировать учётную запись «${u.username}»?`)) return
  await apiFetch(`/staff/cms/users/${u.id}/`, { method: 'DELETE' })
  await load()
  message.value = 'Учётная запись деактивирована'
}

onMounted(() => void load())

</script>



<template>

  <StaffAdminShell>

    <h2 class="admin-h2">Пользователи</h2>

    <p v-if="message" class="admin-ok">{{ message }}</p>

    <p class="admin-muted">Доступ в кабинет сотрудника. Администраторы могут управлять контентом и пользователями.</p>



    <section class="admin-card">

      <div class="admin-table-wrap">
        <table class="admin-table">

          <thead>

            <tr>

              <th>Логин</th>

              <th>Имя</th>

              <th>Email</th>

              <th>Админ</th>

              <th>Менеджер</th>

              <th>Активен</th>

              <th></th>

            </tr>

          </thead>

          <tbody>

            <tr v-for="u in users" :key="u.id">

              <td>{{ u.username }}</td>

              <td><input v-model="u.first_name" class="admin-inp" /></td>

              <td><input v-model="u.email" class="admin-inp" /></td>

              <td><input v-model="u.is_administrator" type="checkbox" /></td>

              <td><input v-model="u.is_manager" type="checkbox" /></td>

              <td><input v-model="u.is_active" type="checkbox" /></td>

              <td class="admin-actions">
                <button type="button" class="admin-btn-sm" @click="saveUser(u)">Сохранить</button>
                <button
                  v-if="u.is_active"
                  type="button"
                  class="admin-btn-sm admin-btn-sm--danger"
                  @click="deactivateUser(u)"
                >
                  Деактивировать
                </button>
              </td>

            </tr>

          </tbody>

        </table>

      </div>

    </section>



    <section class="admin-card">

      <h3>Новый пользователь</h3>

      <div class="admin-grid">

        <input v-model="newUser.username" class="admin-inp" placeholder="Логин" />

        <input v-model="newUser.first_name" class="admin-inp" placeholder="Имя" />

        <input v-model="newUser.email" class="admin-inp" placeholder="Email" type="email" />

        <input v-model="newUser.password" class="admin-inp" placeholder="Пароль" type="password" />

      </div>

      <label class="admin-check">

        <input v-model="newUser.is_administrator" type="checkbox" />

        Администратор

      </label>

      <label class="admin-check">

        <input v-model="newUser.is_manager" type="checkbox" />

        Менеджер

      </label>

      <button type="button" class="admin-btn" @click="createUser">Создать</button>

    </section>

  </StaffAdminShell>

</template>



<style scoped>

@import './admin-shared.css';

.admin-grid {

  display: grid;

  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));

  gap: 8px;

  margin-bottom: 12px;

}

.admin-check {

  display: flex;

  align-items: center;

  gap: 8px;

  margin-bottom: 8px;

}

.admin-actions {

  display: flex;

  flex-wrap: wrap;

  gap: 6px;

}

</style>

