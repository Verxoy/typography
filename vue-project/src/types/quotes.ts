export type QuoteField = {
  key: string
  label: string
  type: 'text' | 'select' | 'textarea'
  placeholder?: string
  required?: boolean
  options?: string[]
}

export type QuoteService = {
  slug: string
  title: string
  hint: string
  fields: QuoteField[]
}

export type QuoteSubmitPayload = {
  service_slug: string
  parameters: Record<string, string>
  company_type: 'ip' | 'ooo' | 'private'
  company_name: string
  inn: string
  contact_name: string
  contact_phone: string
  contact_email: string
  client_comment?: string
}

export type QuoteAttachmentItem = {
  id: number
  original_name: string
  file_size: number
  content_type: string
  uploaded_at: string
  is_image: boolean
  download_url: string
}

export type QuoteListItem = {
  id: number
  public_number: string
  service_title: string
  company_name: string
  inn: string
  contact_name: string
  contact_phone: string
  site_status: string
  has_attachments: boolean
  bitrix_synced_at: string | null
  created_at: string
}

export type QuoteParameterRow = {
  key: string
  label: string
  value: string
}

export type QuoteDetail = QuoteListItem & {
  service_slug: string
  parameters: Record<string, string>
  parameters_labeled?: QuoteParameterRow[]
  company_type: string
  company_type_display: string
  contact_email: string
  client_comment: string
  attachments: QuoteAttachmentItem[]
  site_status_display: string
  manager_note: string
  bitrix_lead_id: number | null
  bitrix_sync_error: string
  bitrix_stub_path: string
}

export const SITE_STATUS_OPTIONS = [
  { value: 'new', label: 'Новая' },
  { value: 'in_review', label: 'В работе' },
  { value: 'kp_sent', label: 'Коммерческое предложение отправлено' },
  { value: 'closed', label: 'Закрыта' },
]
