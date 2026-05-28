/** Порядок карточек разделов на главной (совпадает с Home.vue). */
export const HOME_CATALOG_SECTION_TITLES = [
  'Рекламная полиграфия',
  'Упаковка',
  'Сувениры',
  'Календари',
  'Книги',
  'Рекламная продукция на местах продаж',
  'Полиграфия для медучреждений',
  'Продукция для ресторанов',
] as const

export const HOME_CATALOG_FALLBACK_IMAGES: Record<string, string> = {
  'Рекламная полиграфия': '/images/home-reklamnaya-poligrafiya.png',
  Упаковка: '/images/home-upakovka.png',
  Сувениры: '/images/home-suveniry.png',
  Календари: '/images/home-kalendari.png',
  Книги: '/images/home-knigi.png',
  'Рекламная продукция на местах продаж': '/images/home-reklama-mps.png',
  'Полиграфия для медучреждений': '/images/home-poligrafiya-med.png',
  'Продукция для ресторанов': '/images/home-horeca.png',
}
