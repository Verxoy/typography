export const CALLBACK_STATUS_OPTIONS = [
  { value: 'new', label: 'Новая' },
  { value: 'in_review', label: 'В работе' },
  { value: 'closed', label: 'Перезвонили' },
] as const

export interface CallbackDetail {
  id: number
  public_number: string
  request_type: 'callback'
  type_label: string
  name: string
  phone: string
  site_status: string
  site_status_display: string
  manager_note: string
  bitrix_lead_id: number | null
  bitrix_synced_at: string | null
  bitrix_sync_error: string
  bitrix_stub_path: string
  created_at: string
}
