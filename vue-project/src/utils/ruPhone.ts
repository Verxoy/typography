/** Российский номер: 11 цифр, начинается с 7 (+7 …). */

export const RU_PHONE_PLACEHOLDER = '+7 (999) 999-99-99'

/** Оставляет до 11 цифр, первая — 7. */
export function parseRuPhoneDigits(raw: string): string {
  let digits = raw.replace(/\D/g, '')
  if (!digits) return ''

  if (digits.startsWith('8')) {
    digits = '7' + digits.slice(1)
  } else if (!digits.startsWith('7')) {
    digits = '7' + digits
  }

  return digits.slice(0, 11)
}

/** Маска отображения: +7 (XXX) XXX-XX-XX */
export function formatRuPhone(raw: string): string {
  const digits = parseRuPhoneDigits(raw)
  if (!digits) return ''
  if (digits === '7') return '+7 '

  const rest = digits.slice(1)
  let out = '+7'
  if (rest.length > 0) {
    out += ` (${rest.slice(0, 3)}`
  }
  if (rest.length >= 3) {
    out += `) ${rest.slice(3, 6)}`
  }
  if (rest.length >= 6) {
    out += `-${rest.slice(6, 8)}`
  }
  if (rest.length >= 8) {
    out += `-${rest.slice(8, 10)}`
  }
  return out
}

export function isRuPhoneComplete(value: string): boolean {
  return parseRuPhoneDigits(value).length === 11
}

/** Для отправки на сервер: +79XXXXXXXXX */
export function ruPhoneForApi(value: string): string {
  const digits = parseRuPhoneDigits(value)
  return digits.length === 11 ? `+${digits}` : value.trim()
}
