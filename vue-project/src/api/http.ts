const API_BASE = '/api'

const FIELD_LABELS: Record<string, string> = {
  service_slug: 'Услуга',
  parameters: 'Параметры',
  company_type: 'Тип заказчика',
  company_name: 'Организация',
  inn: 'ИНН',
  contact_name: 'Контактное лицо',
  contact_phone: 'Телефон',
  contact_email: 'Email',
  client_comment: 'Комментарий',
  full_name: 'ФИО',
  age: 'Возраст',
  education: 'Образование',
  position: 'Должность',
  salary: 'Зарплата',
  experience: 'Опыт работы',
  phone: 'Телефон',
  detail: '',
}

function formatApiError(data: unknown, status: number): string {
  if (!data || typeof data !== 'object') {
    return `Ошибка ${status}`
  }
  const obj = data as Record<string, unknown>
  if (typeof obj.detail === 'string') {
    return obj.detail
  }
  const parts: string[] = []
  for (const [field, messages] of Object.entries(obj)) {
    const label = FIELD_LABELS[field] || field
    const list = Array.isArray(messages) ? messages : [messages]
    for (const m of list) {
      const text = typeof m === 'string' ? m : String(m)
      parts.push(label ? `${label}: ${text}` : text)
    }
  }
  if (parts.length) {
    return parts.join(' ')
  }
  return `Ошибка ${status}`
}

function getCookie(name: string): string {
  const match = document.cookie.match(new RegExp(`(?:^|; )${name}=([^;]*)`))
  const value = match?.[1]
  return value ? decodeURIComponent(value) : ''
}

let csrfReady: Promise<void> | null = null

export async function ensureCsrf(): Promise<void> {
  if (getCookie('csrftoken')) return
  if (!csrfReady) {
    csrfReady = fetch(`${API_BASE}/auth/csrf/`, { credentials: 'include' }).then(() => {
      csrfReady = null
    })
  }
  await csrfReady
}

export async function apiFetch<T>(
  path: string,
  options: RequestInit = {},
): Promise<T> {
  const method = (options.method || 'GET').toUpperCase()
  const headers: Record<string, string> = {
    ...(options.headers as Record<string, string>),
  }
  if (options.body && !headers['Content-Type']) {
    headers['Content-Type'] = 'application/json'
  }
  if (!['GET', 'HEAD', 'OPTIONS'].includes(method)) {
    await ensureCsrf()
    const token = getCookie('csrftoken')
    if (token) headers['X-CSRFToken'] = token
  }

  const res = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers,
    credentials: 'include',
  })

  const text = await res.text()
  let data: unknown = null
  if (text) {
    try {
      data = JSON.parse(text)
    } catch {
      data = { detail: text }
    }
  }

  if (!res.ok) {
    throw new Error(formatApiError(data, res.status))
  }
  return data as T
}


export async function apiFetchFormData<T>(
  path: string,
  formData: FormData,
  options: Omit<RequestInit, 'body'> = {},
): Promise<T> {
  const method = (options.method || 'POST').toUpperCase()
  const headers: Record<string, string> = {
    ...(options.headers as Record<string, string>),
  }
  if (!['GET', 'HEAD', 'OPTIONS'].includes(method)) {
    await ensureCsrf()
    const token = getCookie('csrftoken')
    if (token) headers['X-CSRFToken'] = token
  }

  const res = await fetch(`${API_BASE}${path}`, {
    ...options,
    method,
    headers,
    body: formData,
    credentials: 'include',
  })

  const text = await res.text()
  let data: unknown = null
  if (text) {
    try {
      data = JSON.parse(text)
    } catch {
      data = { detail: text }
    }
  }

  if (!res.ok) {
    throw new Error(formatApiError(data, res.status))
  }
  return data as T
}


export async function apiFetchBlob(
  path: string,
  formData: FormData,
  options: Omit<RequestInit, 'body'> = {},
): Promise<Blob> {
  const method = (options.method || 'POST').toUpperCase()
  const headers: Record<string, string> = {
    ...(options.headers as Record<string, string>),
  }
  await ensureCsrf()
  const token = getCookie('csrftoken')
  if (token) headers['X-CSRFToken'] = token

  const res = await fetch(`${API_BASE}${path}`, {
    ...options,
    method,
    headers,
    body: formData,
    credentials: 'include',
  })

  if (!res.ok) {
    const text = await res.text()
    let data: unknown = null
    if (text) {
      try {
        data = JSON.parse(text)
      } catch {
        data = { detail: text }
      }
    }
    const obj = data as Record<string, unknown> | null
    const message =
      (typeof obj?.error === 'string' && obj.error) ||
      formatApiError(data, res.status)
    throw new Error(message)
  }
  return res.blob()
}
