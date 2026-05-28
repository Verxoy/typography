import { apiFetchFormData } from '@/api/http'

export async function uploadCmsImage(
  file: File,
  folder: 'catalog' | 'portfolio' | 'cms' = 'cms',
): Promise<string> {
  const form = new FormData()
  form.append('file', file)
  form.append('folder', folder)
  const res = await apiFetchFormData<{ url: string }>('/staff/cms/upload/', form, {
    method: 'POST',
  })
  return res.url
}

export function resolveMediaUrl(url: string): string {
  if (!url) return ''
  if (url.startsWith('http://') || url.startsWith('https://')) return url
  return url.startsWith('/') ? url : `/${url}`
}
