export type InboxRequestType = 'quote' | 'callback' | 'chat'

export interface InboxListItem {
  id: number
  public_number: string
  request_type: InboxRequestType
  type_label: string
  title: string
  contact_name: string
  phone?: string
  contact_phone?: string
  company_name?: string
  inn?: string
  service_title?: string
  has_attachments?: boolean
  site_status: string
  bitrix_synced_at: string | null
  contact_submitted?: boolean
  created_at: string
}

export type InboxTypeFilter = '' | 'all' | 'quote' | 'callback' | 'chat'
