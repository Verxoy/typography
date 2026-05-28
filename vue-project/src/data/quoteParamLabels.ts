/** Русские подписи полей заявки (в т.ч. старые английские ключи). */
export const QUOTE_PARAM_LABELS: Record<string, string> = {
  opisanie: 'Что нужно сделать',
  tirazh: 'Тираж (если знаете)',
  srok: 'Когда нужно',
  task: 'Что нужно сделать',
  quantity: 'Тираж (если знаете)',
  deadline: 'Когда нужно',
}

export function quoteParamLabel(key: string): string {
  return QUOTE_PARAM_LABELS[key] || key
}
