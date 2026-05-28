import { computed, ref } from 'vue'
import { apiFetch, ensureCsrf } from '@/api/http'

export type StaffUser = {
  id: number
  username: string
  first_name: string
  is_administrator: boolean
  is_manager: boolean
}

const user = ref<StaffUser | null>(null)
const checked = ref(false)
const loading = ref(false)

export function useAuth() {
  const isStaff = computed(() => user.value !== null)
  const isAdministrator = computed(() => Boolean(user.value?.is_administrator))

  async function fetchMe(): Promise<boolean> {
    try {
      user.value = await apiFetch<StaffUser>('/auth/me/')
      return true
    } catch {
      user.value = null
      return false
    } finally {
      checked.value = true
    }
  }

  async function login(username: string, password: string): Promise<void> {
    loading.value = true
    try {
      await ensureCsrf()
      user.value = await apiFetch<StaffUser>('/auth/login/', {
        method: 'POST',
        body: JSON.stringify({ username, password }),
      })
      checked.value = true
    } finally {
      loading.value = false
    }
  }

  async function logout(): Promise<void> {
    await apiFetch('/auth/logout/', { method: 'POST' })
    user.value = null
  }

  return { user, checked, loading, isStaff, isAdministrator, fetchMe, login, logout }
}
