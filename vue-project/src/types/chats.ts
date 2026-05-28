export type ChatStatus = 'bot' | 'waiting_manager' | 'in_progress' | 'closed'

export type ChatSenderType = 'visitor' | 'bot' | 'manager' | 'system'

export interface ChatMessage {
  id: number
  sender_type: ChatSenderType
  text: string
  created_at: string
}

export interface ChatSessionPublic {
  session_key: string
  public_number: string
  visitor_name: string
  email: string
  phone: string
  contact_submitted: boolean
  needs_contact_form: boolean
  status: ChatStatus
  status_display: string
  messages: ChatMessage[]
  created_at: string
  updated_at: string
}

export interface ChatDetail {
  id: number
  public_number: string
  session_key: string
  request_type: 'chat'
  type_label: string
  visitor_name: string
  email: string
  phone: string
  contact_submitted: boolean
  page_url: string
  site_status: ChatStatus
  site_status_display: string
  assigned_to: number | null
  assigned_to_username: string
  manager_note: string
  escalated_at: string | null
  bitrix_lead_id: number | null
  bitrix_synced_at: string | null
  bitrix_sync_error: string
  bitrix_stub_path: string
  created_at: string
  updated_at: string
  messages: ChatMessage[]
}

export const CHAT_STATUS_OPTIONS: { value: ChatStatus; label: string }[] = [
  { value: 'bot', label: 'Бот' },
  { value: 'waiting_manager', label: 'Ожидает менеджера' },
  { value: 'in_progress', label: 'В работе' },
  { value: 'closed', label: 'Закрыт' },
]
